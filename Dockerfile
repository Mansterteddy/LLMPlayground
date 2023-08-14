# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV DLIS_CLIENT_ID=""
ENV DLIS_CLIENT_SECRET=""
ENV DLIS_CLIENT_ENDPOINT="https://WestUS2.bing.prod.dlis.binginternal.com/routestream/aaTest.papyrusplus_stream"

COPY . .

EXPOSE 7000

CMD ["python", "./dlischat.py"]