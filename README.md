# named-entity-recognition

In this project a named entity recognition (NER) model has been trained to detect different fields contained in financial documents (news form Investing.com). Specifically, the entities to be extracted are: PERSON, USER, LOC, DATE, PERCENTAGE, INDEX, ORG and MONEY.

## :gear: Setup
- Clone this repository: `git clone https://github.com/cblancac/named-entity-recognition-hugging-face.git`.
- `pip install requirements.txt`
- This is enough to extract the information from the document (pdfs, images, etc) using Textract or PDFMiner. Textract a OCR tool to extract the information from the document, but PDFMiner is free (although it only works with pdf format). In order to work with a free OCR and images, it would be neccesary to install Pytesseract:
    - `pip install pillow`
    - `sudo apt-get update`
    - `sudo apt install tesseract-ocr`
    - `sudo apt install libtesseract-dev`
    - `pip install pytesseract`


## 	:construction: Data Preparation
The first thing to do in this project is to get a proper dataset. This is a very tedious task, so only 44 document has been labelled in this first version. To do this, you should create a folder called `data`, and inside of it, another folder called `pdfs`, containing all the files to label. Once it is done, run the command `python entry_points/prepare_dataset_to_label.py`. When the process is finished, a new folder `ner_labels` will be created inside of `data`. A csv file will be created per each document, with 2 columns `sentence_id` and `words`. A third column `labels` is needed to be created, which will be used to label manually each word of the document, following the BIO format.


## 	:weight_lifting_man: Training models
Once the dataset is ready, it is time to train the model The model has not been trained from scrach, but a very large pretrained model `xlm-roberta-base` has been taken from `Hugging Face, and later on it has been fine-tuned by using the dataset that was just created. At this way, a lot of time and money has been saved, taking the expert knowledge of the pretrained model over of the English language. To train the model, just execute the command `python entry_points/train.py'
