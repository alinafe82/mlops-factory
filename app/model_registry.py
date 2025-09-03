import mlflow
import numpy as np
from .config import MLFLOW_TRACKING_URI

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

def load_model(model_name: str, stage: str):
    try:
        return mlflow.pyfunc.load_model(f"models:/{model_name}/{stage}")
    except Exception:
        try:
            client = mlflow.client.MlflowClient()
            versions = client.get_latest_versions(model_name, stages=[stage])
            if versions:
                return mlflow.pyfunc.load_model(versions[0].source)
        except Exception:
            return None

def predict_proba(model, X: np.ndarray) -> float:
    if model is None:
        return 0.05
    pred = model.predict(X)
    try:
        pred = np.asarray(pred)
        if pred.ndim == 2 and pred.shape[1] == 2:
            return float(pred[0, 1])
        if pred.ndim == 2 and pred.shape[1] == 1:
            return float(pred[0, 0])
        if pred.ndim == 1:
            val = float(pred[0])
            if val < 0 or val > 1:
                return 1 / (1 + np.exp(-val))
            return val
        return float(pred.flatten()[0])
    except Exception:
        return 0.5
