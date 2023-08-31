ARG PYTHON_VERSION=3.11
ARG ALPINE_VERSION=3.18

# https://hub.docker.com/_/python
ARG BUILDER_IMAGE="python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}"
ARG RUNNER_IMAGE="python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}"

FROM ${BUILDER_IMAGE} as builder

RUN apk add --no-cache --update curl

WORKDIR /app

RUN curl https://cdn.jsdelivr.net/npm/geolite2-city@1.0.0/GeoLite2-City.mmdb.gz | gunzip > GeoLite2-City.mmdb

FROM ${RUNNER_IMAGE}

WORKDIR /app

COPY --from=builder --chown=nobody:root /app/GeoLite2-City.mmdb ./

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY dnsserver.py dnsserver.py

EXPOSE 53

CMD ["python3", "dnsserver.py"]
