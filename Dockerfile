FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN pip install webssh
