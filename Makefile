push:
	(aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 918651736221.dkr.ecr.eu-west-1.amazonaws.com) && \
	docker build -t ner-investing . && \
	docker tag ner-investing:latest 918651736221.dkr.ecr.eu-west-1.amazonaws.com/ner-investing:latest && \
	docker push 918651736221.dkr.ecr.eu-west-1.amazonaws.com/ner-investing:latest \
