import os

os.environ["SKIP_MODEL_LOAD"] = "1"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_infer():
    payload = {"temperature": 60, "vibration": 0.3, "pressure": 30, "rpm": 1500}
    r = client.post("/infer", json=payload)
    assert r.status_code == 200
    assert "defect_probability" in r.json()


def test_infer_500_does_not_leak_exception_detail(monkeypatch):
    """A failing inference must not return Python exception text to the client."""
    import app.main

    def boom(*_args, **_kwargs):
        raise RuntimeError("internal-only: sensitive stack-style message")

    monkeypatch.setattr(app.main, "predict_proba", boom)

    payload = {"temperature": 60, "vibration": 0.3, "pressure": 30, "rpm": 1500}
    r = client.post("/infer", json=payload)
    assert r.status_code == 500
    body = r.json()
    assert "internal-only" not in str(body)
    assert "sensitive" not in str(body)
    assert body == {"detail": "Inference failed"}


def test_infer_rejects_non_finite_measurements():
    payload = {"temperature": "NaN", "vibration": 0.3, "pressure": 30, "rpm": 1500}
    response = client.post("/infer", json=payload)

    assert response.status_code == 422


def test_infer_rejects_out_of_range_model_probability(monkeypatch):
    import app.main

    monkeypatch.setattr(app.main, "predict_proba", lambda *_args, **_kwargs: 1.5)
    payload = {"temperature": 60, "vibration": 0.3, "pressure": 30, "rpm": 1500}

    response = client.post("/infer", json=payload)

    assert response.status_code == 500
    assert response.json() == {"detail": "Inference failed"}
