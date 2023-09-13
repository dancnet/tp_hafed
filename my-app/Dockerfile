FROM python:3.9
WORKDIR /app
COPY app/ ./
RUN apt-get update && apt-get install -y default-jre && pip install pyspark kafka-python happybase
