import time

import numpy as np
from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel
from starlette.responses import Response

from .config import MLFLOW_TRACKING_URI, MODEL_NAME, MODEL_STAGE, SKIP_MODEL_LOAD
from .model_registry import load_model, predict_proba
from .monitoring.drift import update_input_stats
from .monitoring.metrics import INFERENCE_ERRORS, INFLIGHT, REQUEST_COUNT, REQUEST_LATENCY

app = FastAPI(title="MLOps Factory Inference", version="1.0.0")

model = None


class InferenceRequest(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    rpm: float


class InferenceResponse(BaseModel):
    ok: bool
    defect_probability: float


@app.on_event("startup")
def _startup():
    global model
    if SKIP_MODEL_LOAD:
        return
    model = load_model(MODEL_NAME, MODEL_STAGE)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "model_loaded": model is not None, "tracking_uri": MLFLOW_TRACKING_URI}


@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.post("/infer", response_model=InferenceResponse)
def infer(req: InferenceRequest):
    start = time.time()
    INFLIGHT.inc()
    status = "200"
    try:
        x = np.array([req.temperature, req.vibration, req.pressure, req.rpm], dtype=float).reshape(
            1, -1
        )
        update_input_stats(x[0])
        p = predict_proba(model, x)
        return {"ok": True, "defect_probability": float(p)}
    except Exception as e:
        INFERENCE_ERRORS.inc()
        status = "500"
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        REQUEST_LATENCY.observe(time.time() - start)
        REQUEST_COUNT.labels(endpoint="/infer", method="POST", status=status).inc()
        INFLIGHT.dec()
