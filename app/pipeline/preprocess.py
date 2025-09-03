from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

FEATURES = ["temperature", "vibration", "pressure", "rpm"]

def make_preprocessor():
    scaler = Pipeline(steps=[("scaler", StandardScaler())])
    pre = ColumnTransformer(
        transformers=[("num", scaler, FEATURES)]
    )
    return pre
