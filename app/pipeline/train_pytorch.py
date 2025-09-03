import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
import mlflow.pytorch
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from .data import synthesize

class MLP(nn.Module):
    def __init__(self, in_dim=4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)

def run_pytorch(model_name: str, stage: str = None, epochs: int = 10, batch_size: int = 64):
    X, y = synthesize()
    X_train, X_test, y_train, y_test = train_test_split(X.values, y, test_size=0.2, random_state=7)

    device = torch.device("cpu")
    model = MLP().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.BCELoss()

    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train.reshape(-1,1), dtype=torch.float32)

    model.train()
    with mlflow.start_run(run_name=f"torch_{model_name}"):
        n = X_train_t.shape[0]
        for epoch in range(epochs):
            perm = torch.randperm(n)
            for i in range(0, n, batch_size):
                idx = perm[i:i+batch_size]
                xb = X_train_t[idx]
                yb = y_train_t[idx]
                optimizer.zero_grad()
                out = model(xb)
                loss = criterion(out, yb)
                loss.backward()
                optimizer.step()

        model.eval()
        with torch.no_grad():
            X_test_t = torch.tensor(X_test, dtype=torch.float32)
            proba = model(X_test_t).numpy().reshape(-1)
        auc = roc_auc_score(y_test, proba)
        mlflow.log_metric("auc", float(auc))
        mlflow.pytorch.log_model(model, artifact_path="model", registered_model_name=model_name)

        if stage:
            client = mlflow.client.MlflowClient()
            mv = client.get_latest_versions(model_name)[-1]
            client.transition_model_version_stage(model_name, mv.version, stage, archive_existing_versions=True)
            print(f"Registered and promoted '{model_name}' to stage '{stage}', AUC={auc:.3f}")
