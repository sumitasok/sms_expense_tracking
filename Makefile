cp_sms_db:
	cp ~/Library/Messages/chat.db data/

setup: build
	npm install -g serverless

# make serverless RUN_ARGS='create --template aws-python3 --name mongodb --path mongodb' (step-1)
serverless:
	docker run -it -v `pwd`:/src --rm serverless:latest serverless $(RUN_ARGS)

# make serverless_create NAME=mongodb PATH=mongodb
serverless_create:
	make serverless RUN_ARGS='create --template aws-python3 --name $(NAME) --path $(PATH)'

build:
	docker-compose -f "docker-compose.yml" up -d --build 


# create .aws folder and copy your config and credential to the same.