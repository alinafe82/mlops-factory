import logging
import time
from contextlib import asynccontextmanager

import numpy as np
from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel
from starlette.responses import Response

logger = logging.getLogger(__name__)

from .config import MLFLOW_TRACKING_URI, MODEL_NAME, MODEL_STAGE, SKIP_MODEL_LOAD
from .model_registry import load_model, predict_proba
from .monitoring.drift import update_input_stats
from .monitoring.metrics import (
    INFERENCE_ERRORS,
    INFLIGHT,
    REQUEST_COUNT,
    REQUEST_LATENCY,
)

model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    if not SKIP_MODEL_LOAD:
        model = load_model(MODEL_NAME, MODEL_STAGE)
    yield


app = FastAPI(title="MLOps Factory Inference", version="1.0.0", lifespan=lifespan)


class InferenceRequest(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    rpm: float


class InferenceResponse(BaseModel):
    ok: bool
    defect_probability: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    tracking_uri: str


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(
        status="ok",
        model_loaded=model is not None,
        tracking_uri=MLFLOW_TRACKING_URI,
    )


@app.get("/metrics", response_model=None)
def metrics() -> Response:
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.post("/infer", response_model=InferenceResponse)
def infer(req: InferenceRequest) -> InferenceResponse:
    start = time.time()
    INFLIGHT.inc()
    status = "200"
    try:
        x = np.array(
            [req.temperature, req.vibration, req.pressure, req.rpm], dtype=float
        ).reshape(1, -1)
        update_input_stats(x[0])
        p = predict_proba(model, x)
        return InferenceResponse(ok=True, defect_probability=float(p))
    except Exception:
        INFERENCE_ERRORS.inc()
        status = "500"
        logger.exception("Inference failed")
        raise HTTPException(status_code=500, detail="Inference failed")
    finally:
        REQUEST_LATENCY.observe(time.time() - start)
        REQUEST_COUNT.labels(endpoint="/infer", method="POST", status=status).inc()
        INFLIGHT.dec()
