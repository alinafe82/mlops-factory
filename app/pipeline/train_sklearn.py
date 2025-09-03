import mlflow
import mlflow.sklearn
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from .data import synthesize
from .preprocess import make_preprocessor, FEATURES

def run_sklearn(model_name: str, stage: str = None):
    X, y = synthesize()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)

    pipe = Pipeline(steps=[
        ("pre", make_preprocessor()),
        ("clf", LogisticRegression(max_iter=300))
    ])

    with mlflow.start_run(run_name=f"sklearn_{model_name}"):
        pipe.fit(X_train[FEATURES], y_train)
        proba = pipe.predict_proba(X_test[FEATURES])[:,1]
        auc = roc_auc_score(y_test, proba)
        mlflow.log_metric("auc", float(auc))
        mlflow.sklearn.log_model(pipe, "model", registered_model_name=model_name)

        if stage:
            client = mlflow.client.MlflowClient()
            mv = client.get_latest_versions(model_name)[-1]
            client.transition_model_version_stage(model_name, mv.version, stage, archive_existing_versions=True)
            print(f"Registered and promoted '{model_name}' to stage '{stage}', AUC={auc:.3f}")
