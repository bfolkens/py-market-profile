FROM python:3

WORKDIR /workspace

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./
