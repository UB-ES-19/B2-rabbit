FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /rabbitApp
WORKDIR /rabbitApp
COPY /rabbitApp/requirements.txt /rabbitApp
RUN pip install -r requirements.txt
COPY . /rabbitApp/
