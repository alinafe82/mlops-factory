PY=python
PIP=pip

install:
	$(PIP) install --upgrade pip
	test -f app/requirements-base.txt && $(PIP) install -r app/requirements-base.txt
	# Uncomment if you want heavy ML deps locally:
	# test -f app/requirements-ml.txt && $(PIP) install -r app/requirements-ml.txt

train:
	MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI:-file:./mlruns} $(PY) app/pipeline/cli.py train --framework sklearn --name ${MODEL_NAME:-factory-model} --stage ${MODEL_STAGE:-Staging}

run:
	SKIP_MODEL_LOAD=1 uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

test:
	PYTHONPATH=. pytest -q

lint:
	flake8 app tests

compose-mlflow:
	docker compose -f docker-compose.mlflow.yml up -d

docker-build:
	docker build -t alinafe/mlops-factory:latest .

docker-run:
	docker run -e SKIP_MODEL_LOAD=1 -p 8000:8000 alinafe/mlops-factory:latest
