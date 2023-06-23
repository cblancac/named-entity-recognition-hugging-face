from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from dataset.dataset          import Dataset
from train_model.ner_trainer import NerTrainer

NUM_EPOCHS = 1 #3
BATCH_SIZE = 1 #24

datasets_path = Path("data/ner_labels/")
dataset_filename = Path("dataset.csv")
model_ckpt = Path("xlm-roberta-base")


def train_pipeline():
    data = Dataset(datasets_path, dataset_filename)

    # Generate dataset.csv concatenating all sigles dataset
    data.create_dataset_csv()
    
    # Generate test_dataset.csv and train_dataset.csv
    data.split_train_test(train_size=0.8)

    _train(model_ckpt, data)

def _train(model_ckpt, data):
    dataset, dict_int2str, dict_str2int, num_classes = data.load_hf_dataset()
    ner = NerTrainer(
        model_ckpt=model_ckpt,
        data=dataset,
        int2str=dict_int2str,
        str2int=dict_str2int,
        num_classes=num_classes,
        n_epochs=NUM_EPOCHS,
        batch_size=BATCH_SIZE,
    )
    ner.train_model()