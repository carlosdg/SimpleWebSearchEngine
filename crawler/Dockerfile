FROM python:3.7

WORKDIR /container

RUN pip install aiohttp[speedups] beautifulsoup4 umongo[motor]

COPY src .
COPY config .