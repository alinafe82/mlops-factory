import numpy as np
import pandas as pd


def synthesize(n=5000, seed=42):
    rng = np.random.default_rng(seed)
    temperature = rng.normal(60, 5, n)
    vibration = rng.normal(0.3, 0.05, n)
    pressure = rng.normal(30, 2, n)
    rpm = rng.normal(1500, 100, n)
    defect = (temperature > 65) | (vibration > 0.4) | (pressure < 28) | (rpm > 1650)
    y = defect.astype(int)
    X = pd.DataFrame(
        {
            "temperature": temperature,
            "vibration": vibration,
            "pressure": pressure,
            "rpm": rpm,
        }
    )
    return X, y
