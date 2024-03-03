# named-entity-recognition

In this project a named entity recognition (NER) model has been trained to detect different fields contained in financial documents (news form Investing.com). Specifically, the entities to be extracted are: PERSON, USER, LOC, DATE, PERCENTAGE, INDEX, ORG and MONEY.

## :gear: Setup
- Clone this repository: `git clone https://github.com/cblancac/named-entity-recognition-hugging-face.git`.
- `pip install requirements.txt`
- `sudo yum install poppler-utils`
- This is enough to extract the information from the document (pdfs, images, etc) using Textract or PDFMiner. Textract is a OCR tool to extract the information from the document (having access also to their coordinates), but PDFMiner is free (although it only works with pdf format). In order to work with a free OCR and images, it would be neccesary to install Pytesseract:
    - `pip install pillow`
    - `sudo apt-get update`
    - `sudo apt install tesseract-ocr`
    - `sudo apt install libtesseract-dev`
    - `pip install pytesseract`

- To train this model, an instance EC2 (Elastic Compute Cloud) of AWS has been used. More specifically, the type of instance used has been `g4dn.xlarge`, which has allowed us to use GPU.
- An instance with an attached NVIDIA GPU, such as `g4dn.xlarge`, must have the appropriate NVIDIA driver installed. Follow this tutorial to get the appropiate NVIDIA driver: `https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html` (in my case, section Option 3: GRID drivers (G5, G4dn, and G3 instances)


## 	:construction: Data Preparation
The first thing to do in this project is to get a proper dataset. This is a very tedious task, so only 44 document has been labelled in this first version. To do this, you should create a folder called `data`, and inside of it, another folder called `pdfs`, containing all the files to label. Once it is done, you are ready to run the command `python entry_points/prepare_dataset_to_label.py`. This script will upload all the documents inside of 'pdfs' folder to S3 (in the bucket and folder that you select). Then Textract will be called, once per document, extracting the information of their content and coordinates, saving them in you machine:
- `txts`: content of the document.
- `jsons`: information of coordinates.
- `ner_labels`: with the csv of the document with 3 columns, `sentence_id` (phrase to which each word belongs), `words` (for each word in the document) and `labels` (initially empty, and need to be labelled manually, following the following the BIO format).


## 	:weight_lifting_man: Training models
Once the dataset is ready, it is time to train the model The model has not been trained from scrach, but a very large pretrained model `xlm-roberta-base` has been taken from `Hugging Face`, and later on it has been fine-tuned by using the dataset that was just created. At this way, a lot of time and money has been saved, taking the expert knowledge of the pretrained model over of the English language. To train the model, just execute the command `python entry_points/train.py'. After a few minutes, the model will be fine-tuned and storage in your machine, showing in your terminal the metrics achieved by epoch. Only with these 44 documents, an 80% f1 score has been achieved, which is actually a very good result to have been fine-tuned with such a small dataset.
