# python3.8 lambda base image
FROM public.ecr.aws/lambda/python:3.8

# copy requirements.txt to container
COPY requirements.txt ./

# installing dependencies
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy function code to container
COPY app.py ./
COPY model.py ./

# Copy model to container
RUN mkdir models
COPY models ./models 

# Copy the neccesaries folders to container
RUN mkdir cloud_service
RUN mkdir dataset
RUN mkdir utils
RUN mkdir entidades
RUN mkdir inference_model

COPY cloud_service ./cloud_service
COPY dataset ./dataset
COPY utils ./utils
COPY entidades ./entidades
COPY inference_model ./inference_model

# setting the CMD to your handler file_name.function_name
CMD [ "app.handler" ]
