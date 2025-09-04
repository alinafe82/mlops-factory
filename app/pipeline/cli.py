import click

from ..config import MODEL_NAME
from .train_pytorch import run_pytorch
from .train_sklearn import run_sklearn
from .train_tensorflow import run_tensorflow


@click.group()
def cli():
    """MLOps Factory pipeline CLI"""
    pass


@cli.command()
@click.option(
    "--framework",
    type=click.Choice(["sklearn", "tensorflow", "pytorch"]),
    default="sklearn",
)
@click.option("--name", default=MODEL_NAME, help="Registered model name")
@click.option(
    "--stage", default=None, help="Stage to promote to (e.g., Staging, Production)"
)
def train(framework, name, stage):
    if framework == "sklearn":
        run_sklearn(name, stage)
    elif framework == "tensorflow":
        run_tensorflow(name, stage)
    else:
        run_pytorch(name, stage)


if __name__ == "__main__":
    cli()
