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
- An instance with an attached NVIDIA GPU, such as `g4dn.xlarge`, must have the appropriate NVIDIA driver installed. Follow this tutorial to get the appropiate NVIDIA driver: `https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html` (in my case, section Option 3: GRID drivers (G5, G4dn, and G3 instances)).


## 	:construction: Data Preparation
The first thing to do in this project is to get a proper dataset. This is a very tedious task, so only 44 document has been labelled in this first version. To do this, you should create a folder called `data`, and inside of it, another folder called `pdfs`, containing all the files to label. Once it is done, you are ready to run the command `python entry_points/prepare_dataset_to_label.py`. This script will upload all the documents inside of 'pdfs' folder to S3 (in the bucket and folder that you select). Then Textract will be called, once per document, extracting the information of their content and coordinates, saving them in your machine:
- `txts`: content of the document.
- `jsons`: information of coordinates.
- `ner_labels`: with the csv of the document with 3 columns, `sentence_id` (phrase to which each word belongs), `words` (for each word in the document) and `labels` (initially empty, and need to be labelled manually, following the following the BIO format).


## 	:weight_lifting_man: Training models
Once the dataset is ready, it is time to train the model The model has not been trained from scrach, but a very large pretrained model `xlm-roberta-base` has been taken from `Hugging Face`, and later on it has been fine-tuned by using the dataset that was just created. At this way, a lot of time and money has been saved, taking the expert knowledge of the pretrained model over of the English language. To train the model, just execute the command `python entry_points/train.py`.

![image](https://github.com/cblancac/named-entity-recognition-hugging-face/assets/105242658/f686ebfa-42ef-42b8-912f-d927b882fbfa)

After a few minutes, the model will be fine-tuned and storage in your machine (in the `models` folder), showing in your terminal the metrics achieved by epoch. Only with these 44 documents, an 80% f1 score has been achieved, which is actually a very good result to have been fine-tuned with such a small dataset.


## :tada: Make predictions
Finally the prediction of the entities present in the document can be extracted running the script python entry_points/inference.py. Executing this script, we will have to introduce the filename of one of our filenames (in the folder data/pdfs) as input and it will give us back a dictionary with the entities (DATE, ORG, INDEX, LOC, PERSON, PERCENTAGE, PERCENTAGE, PERSON, INDEX, MONEY, and USER) detected in the document by the model. Before we get the output, we will be asked to choose our favourite OCR to read the content from the document:

* **pdf**: to use PDF Miner
* **aws**: to use Textract
* **img**: to use Pytesseract

All the files generated for the Named Entity Recognition model has been uploaded to my Hugging Face account, with the requirements.txt and the script necessary to run inference using Gradio. You could tested directly from my [Hugging Face Spaces]([https://huggingface.co/spaces/carblacac/emotion-detection](https://huggingface.co/spaces/carblacac/ner-investing))

You only need to choose a file to be processed or choose the one I uploaded as an example: 
![image](https://github.com/cblancac/named-entity-recognition-hugging-face/assets/105242658/b370f999-437e-4dfe-a957-2a6677a7674f)


The result will be something similar to this:

![image](https://github.com/cblancac/named-entity-recognition-hugging-face/assets/105242658/9a2c0df0-fcbd-444b-a140-43d4cf4d4fac)



## :airplane: Deployment

0. **IAM**:

The first step to deploy the model is to attach a new policy to your IAM role: `AmazonEC2ContainerRegistryFullAccess` 

![image](https://github.com/cblancac/named-entity-recognition-hugging-face/assets/105242658/c27046b0-208f-4ad8-be18-72b96280bed0)


1. **EC2**:
In the root folder folder it is needed to add the next files:
  * `Dockerfile`: configuration file used to build a Docker image.
  * `app.py`: Python file containing the code for the application.
  * `models/xlm-roberta-base-investing-ner`: directory containing data for the fine-tuned model.
  * `exceptions.py`: Python file that contain definitions of custom exceptions used in the application.
  * `requirements.txt`: file containing a list of Python dependencies required for the application.

2. **ECR**:
Once all the necessary files and folders have been created in EC2, it is time to create a repository.

![image](https://github.com/user-attachments/assets/7571a9cb-69c9-4b67-b478-506b077300b1)

When it is created, click on it and click on the box to "View push commands". This will show all the commands that need to be executed from the terminal in EC2.

3. **Lambda Function**:
The next step is to create a Lambda function. Go to the Lambda service and click on "Create a function". 
![image](https://github.com/user-attachments/assets/539bad35-4ab1-4468-863c-98bf1efaffaf)

Select the container image box, give a name to the lambda function and click on "Browse images":
![image](https://github.com/user-attachments/assets/9beb4d53-99b0-482a-9d7b-726c6325b962)

