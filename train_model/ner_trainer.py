import numpy as np
import torch
from transformers import AutoTokenizer
from transformers import DataCollatorForTokenClassification
from transformers import Trainer
from transformers import TrainingArguments

from config import InvestingConfig
from dataset.tokenize_dataset import TokenizeDataset
from model  import XLMRobertaForTokenClassification
from seqeval.metrics import f1_score


class NerTrainer:
    def __init__(
        self, model_ckpt, data, int2str, str2int, num_classes, n_epochs, batch_size
    ):
        self.model_ckpt = model_ckpt
        self.data = data
        self.int2str = int2str
        self.str2int = str2int
        self.num_classes = num_classes
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.config = self.get_config()

    def train_model(self):
        dataset_encoded = self.tokenize_dataset()

        logging_steps = len(dataset_encoded["train"]) // self.batch_size
        model_name = f"models/{self.model_ckpt}-investing-ner"
        training_args = TrainingArguments(
            output_dir=model_name, log_level="error", num_train_epochs=self.n_epochs,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            save_steps=1e6, weight_decay=0.01, disable_tqdm=False,
            logging_steps=logging_steps, push_to_hub=False)
        
        data_collator = DataCollatorForTokenClassification(AutoTokenizer.from_pretrained(self.model_ckpt))

        trainer = Trainer(model_init=self.model_init, args=training_args,
                data_collator=data_collator, compute_metrics=self.compute_metrics,
                train_dataset=dataset_encoded["train"],
                eval_dataset=dataset_encoded["test"],
                tokenizer=AutoTokenizer.from_pretrained(self.model_ckpt))
        
        trainer.train()
        trainer.save_model(model_name)

    def get_config(self):
        inv_config = InvestingConfig(
            self.model_ckpt, self.num_classes, self.int2str, self.str2int
        )
        return inv_config.get_config()
    
    def tokenize_dataset(self):
        tokenizer = TokenizeDataset(self.model_ckpt)
        return tokenizer.encode_dataset(self.data)
    
    def model_init(self):
        return (XLMRobertaForTokenClassification
                .from_pretrained(self.model_ckpt, config=self.config)
                .to(self.device))

    def compute_metrics(self, eval_pred):
        y_pred, y_true = self._align_predictions(eval_pred.predictions,
                                        eval_pred.label_ids)
        return {"f1": f1_score(y_true, y_pred)}

    def _align_predictions(self, predictions, label_ids):
        preds = np.argmax(predictions, axis=2)
        batch_size, seq_len = preds.shape
        labels_list, preds_list = [], []
        
        for batch_idx in range(batch_size):
            examples_labels, examples_preds = [], []
            for seq_idx in range(seq_len):
                # Ignore label IDs = -100
                if label_ids[batch_idx, seq_idx] != 100:
                    examples_labels.append(self.int2str[label_ids[batch_idx][seq_idx]])
                    examples_preds.append(self.int2str[preds[batch_idx][seq_idx]])
                    
            labels_list.append(examples_labels)
            preds_list.append(examples_preds)
            
            return preds_list, labels_list