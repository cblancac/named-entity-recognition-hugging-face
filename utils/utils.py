import os
from pathlib import Path


def makedirs(path: Path) -> None:
    """Create a directory if it does not exist."""
    if not os.path.isdir(path):
        os.makedirs(path)
