FROM node:13.8.0-alpine3.10

RUN npm install -g serverless

WORKDIR /src