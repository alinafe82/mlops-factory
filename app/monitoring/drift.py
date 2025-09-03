import numpy as np
from .metrics import INPUT_MEAN, INPUT_STD

WINDOW = 200
_buf = []

FEATURES = ["temperature", "vibration", "pressure", "rpm"]

def update_input_stats(x):
    global _buf
    _buf.append(x)
    if len(_buf) > WINDOW:
        _buf[:] = _buf[-WINDOW:]
    arr = np.array(_buf)
    means = arr.mean(axis=0)
    stds = arr.std(axis=0)
    for i, name in enumerate(FEATURES):
        INPUT_MEAN.labels(feature=name).set(float(means[i]))
        INPUT_STD.labels(feature=name).set(float(stds[i]))
