FROM python:3.7-slim

WORKDIR /backend

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . ./

ENTRYPOINT [ "tail", "-f", "/dev/null" ]