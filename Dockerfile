# app/Dockerfile
FROM python:3.10.6

WORKDIR /app

#RUN apt-get update && apt-get install -y \
#    build-essential \
#    curl \
#    software-properties-common \
#    git \
#    && rm -rf /var/lib/apt/lists/*
#
#RUN git clone https://github.com/streamlit/streamlit-example.git .

COPY ./1_Login_Page.py ./requirements.txt  /app/

COPY ./aws_logging.py /app/

COPY ./Util /app/Util

COPY ./Authentication /app/Authentication

COPY ./pages /app/pages

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "1_Login_Page.py"]