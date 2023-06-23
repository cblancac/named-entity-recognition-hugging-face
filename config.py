from transformers import AutoConfig

class InvestingConfig():
    def __init__(
            self,
            model_name,
            num_classes,
            index2tag,
            tag2index,
    ):
        self.model_name  = model_name
        self.num_classes = num_classes
        self.index2tag   = index2tag
        self.tag2index   = tag2index
        
    def get_config(self):
        return AutoConfig.from_pretrained(self.model_name,
                                          num_labels=self.num_classes,
                                          id2label=self.index2tag, 
                                          label2id=self.tag2index
                                          )