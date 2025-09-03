# Production container for MLOps Factory (CPU)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git curl && rm -rf /var/lib/apt/lists/*

COPY app/requirements-base.txt app/requirements-ml.txt /app/app/
RUN pip install --no-cache-dir -r app/requirements-base.txt
RUN pip install --no-cache-dir -r app/requirements-ml.txt

COPY app /app/app

EXPOSE 8080

ENV MODEL_NAME=factory_defect_model     MODEL_STAGE=Production     MLFLOW_TRACKING_URI=file:/models/mlruns

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
