### Step 1
# make virtualenv RUN_ARGS='venv --python=python3'
virtualenv:
	docker run -it -v `pwd`:/src --rm virtualenv:latest virtualenv $(RUN_ARGS)

source_activate:
	docker run -it -v `pwd`:/src --rm virtualenv:latest /bin/bash

venv_py3: # (step-2)
	make virtualenv RUN_ARGS='venv --python=python3'

# Step 2
# make source_activate
# Once entered the above command, terminal will open
# issue the below commands
# $ source venv/bin/activate
# pip install pymongo
# pip freeze > requirements.txt

serverless:
	docker run -it -v `pwd`:/src -v `pwd`/.aws:/root/.aws --rm serverless:latest serverless $(RUN_ARGS)

npm:
	docker run -it -v `pwd`:/src -v `pwd`/.aws:/root/.aws --rm serverless:latest npm $(RUN_ARGS)

# create .aws folder and copy your config and credential to the same.

# Step 3:
# make npm RUN_ARGS='init'
# Step 4:
# make npm RUN_ARGS='install --save serverless-python-requirements'

# https://serverless-stack.com/chapters/configure-multiple-aws-profiles.html
# serverless deploy --aws-profile sumit

# serverless invoke -f mongodb --log --aws-profile sumit