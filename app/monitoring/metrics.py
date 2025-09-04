from prometheus_client import Counter, Gauge, Histogram

REQUEST_COUNT = Counter(
    "api_requests_total", "Total API requests", ["endpoint", "method", "status"]
)
REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API request latency (seconds)",
    buckets=(0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5),
)
INFERENCE_ERRORS = Counter("inference_errors_total", "Total inference failures")
INFLIGHT = Gauge("api_inflight_requests", "In-flight requests")

INPUT_MEAN = Gauge("input_feature_mean", "Rolling mean per feature", ["feature"])
INPUT_STD = Gauge("input_feature_std", "Rolling std per feature", ["feature"])
