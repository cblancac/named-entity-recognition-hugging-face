# named-entity-recognition

In this project a named entity recognition (NER) model has been trained to detect different fields contained in financial documents (news form Investing.com). Specifically, the entities to be extracted are: PERSON, USER, LOC, DATE, PERCENTAGE, INDEX, ORG and ORG.

## :gear: Setup
- Clone this repository: `git clone https://github.com/cblancac/named-entity-recognition-hugging-face.git`.
- `pip install requirements.txt`
- This is enough to extract the information from the document (pdfs, images, etc) using Textract or PDFMiner. Textract a OCR tool to extract the information from the document, but PDFMiner is free (although it only works with pdf format). In order to work with a free OCR and images, it would be neccesary to install Pytesseract:
    - pip install pillow
    - sudo apt-get update
    - sudo apt install tesseract-ocr
    - sudo apt install libtesseract-dev
    - pip install pytesseract
