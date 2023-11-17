FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN mkdir /usr/prod_api/
WORKDIR /usr/prod_api/
COPY ../../requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
