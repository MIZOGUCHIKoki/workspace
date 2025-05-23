FROM python:3-slim

RUN apt-get update \
	&& apt-get install -y --no-install-recommends vim less \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /root/

COPY requirements.txt .

RUN pip install --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt