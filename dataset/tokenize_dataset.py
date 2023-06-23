from transformers import AutoTokenizer


class TokenizeDataset():
    def __init__(self, model_ckpt):
        self.model_ckpt = model_ckpt
        self.tokenizer = self._tokenizer()

    def encode_dataset(self, corpus):
        return corpus.map(self._tokenize_and_align_labels, batched=True,
                        remove_columns=['idx_sentence', 'filename', 'tokens'])
    
    def _tokenize_and_align_labels(self, examples):
        tokenized_inputs = self.tokenizer(examples["tokens"], truncation=True,
                                        is_split_into_words=True)
        labels = []
        for idx, label in enumerate(examples["ner_tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=idx)
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                if word_idx is None or word_idx == previous_word_idx:
                    label_ids.append(-100)
                else:
                    label_ids.append(label[word_idx])
                previous_word_idx = word_idx
            labels.append(label_ids)
        tokenized_inputs["labels"] = labels
        return tokenized_inputs
    
    def _tokenizer(self):
        return AutoTokenizer.from_pretrained(self.model_ckpt)
