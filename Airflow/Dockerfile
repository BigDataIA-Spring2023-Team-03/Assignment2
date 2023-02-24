# app/Dockerfile
FROM python:3.10.6
# Base docker image of python 3.x

RUN pip install --upgrade pip


#RUN apt-get update && apt-get install -y \
#    build-essential \
#    curl \
#    software-properties-common \
#    git \
#    && rm -rf /var/lib/apt/lists/*
#
#RUN git clone https://github.com/streamlit/streamlit-example.git .

FROM apache/airflow:2.5.1
USER root
WORKDIR /app
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow

RUN pip install --no-cache-dir lxml

COPY ./dags app/dags
COPY ../requirements.txt /app/
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["airflow", "standalone"]

