FROM python:3.7.9-stretch

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools

COPY requirements.txt /tmp/requirements.txt
RUN cat /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /opt/app
