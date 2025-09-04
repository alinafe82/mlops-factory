from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["temperature", "vibration", "pressure", "rpm"]


def make_preprocessor():
    scaler = Pipeline(steps=[("scaler", StandardScaler())])
    pre = ColumnTransformer(transformers=[("num", scaler, FEATURES)])
    return pre
