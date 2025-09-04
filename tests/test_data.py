from app.pipeline.data import synthesize


def test_synthesize():
    X, y = synthesize(n=100)
    assert len(X) == 100
    assert len(y) == 100
