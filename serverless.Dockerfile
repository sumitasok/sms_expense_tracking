FROM node:13.8.0-alpine3.10

RUN npm install -g serverless
# https://github.com/colynb/serverless-dotenv-plugin
RUN npm i -D serverless-dotenv-plugin

WORKDIR /src