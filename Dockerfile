FROM python:3.8.0-slim

RUN pip install --upgrade pip
RUN pip install db-sqlite3
RUN pip install pymongo
RUN pip install dnspython
RUN pip install pymodm
RUN pip install pandas

WORKDIR /src