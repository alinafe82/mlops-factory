FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY app/requirements-base.txt /app/requirements-base.txt
RUN pip install --no-cache-dir -r /app/requirements-base.txt

# Optional heavy ML deps:
# COPY app/requirements-ml.txt /app/requirements-ml.txt
# RUN pip install --no-cache-dir -r /app/requirements-ml.txt

COPY app /app/app
COPY ops/start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000
CMD ["/app/start.sh"]
