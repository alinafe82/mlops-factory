import mlflow
import mlflow.tensorflow
import tensorflow as tf
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from .data import synthesize


def run_tensorflow(model_name: str, stage: str = None):
    X, y = synthesize()
    X_train, X_test, y_train, y_test = train_test_split(X.values, y, test_size=0.2, random_state=7)

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(4,)),
            tf.keras.layers.Normalization(),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.layers[0].adapt(X_train)

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["AUC"])
    with mlflow.start_run(run_name=f"tf_{model_name}"):
        model.fit(X_train, y_train, epochs=10, batch_size=64, verbose=0, validation_split=0.1)
        proba = model.predict(X_test, verbose=0).reshape(-1)
        auc = roc_auc_score(y_test, proba)
        mlflow.log_metric("auc", float(auc))
        mlflow.tensorflow.log_model(
            tf_model=model, artifact_path="model", registered_model_name=model_name
        )

        if stage:
            client = mlflow.client.MlflowClient()
            mv = client.get_latest_versions(model_name)[-1]
            client.transition_model_version_stage(
                model_name, mv.version, stage, archive_existing_versions=True
            )
            print(f"Registered and promoted '{model_name}' to stage '{stage}', AUC={auc:.3f}")
