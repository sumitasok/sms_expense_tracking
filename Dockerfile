FROM python:3.8.0-alpine3.10

RUN pip install db-sqlite3
RUN pip install pymongo
RUN pip install dnspython

WORKDIR /src