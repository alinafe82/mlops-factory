import os

# Model registry / tracking
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
MODEL_NAME = os.getenv("MODEL_NAME", "factory_defect_model")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Production")  # e.g., Staging, Production

# API behavior
SKIP_MODEL_LOAD = bool(int(os.getenv("SKIP_MODEL_LOAD", "0")))  # for CI
