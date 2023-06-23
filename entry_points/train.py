from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from entidades.engines.neural.train_pipeline import train_pipeline


if __name__ == '__main__':
    train_pipeline()