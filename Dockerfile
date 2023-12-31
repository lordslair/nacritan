FROM alpine:3.18

RUN adduser -h /code -u 1000 -D -H api

ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY --chown=api:api requirements.txt /code/requirements.txt
COPY --chown=api:api /code            /code

WORKDIR /code
ENV PATH="/code/.local/bin:${PATH}"

RUN apk update --no-cache \
    && apk add --no-cache \
        "libjpeg>=9e-r1" \
        "python3>=3.11" \
        "py3-pip>=23" \
        "tzdata>=2023" \
    && apk add --no-cache --virtual .build-deps \
        "gcc=~12" \
        "libc-dev=~0.7" \
        "python3-dev>=3.11" \
        "g++=~12" \
        "jpeg-dev>=9e-r1" \
        "libffi-dev>=3.4.4-r2" \
        "zlib-dev>=1.2.13-r1" \
    && su api -c \
        "pip3 install --break-system-packages --user -U -r requirements.txt && \
        rm requirements.txt" \
    && apk del .build-deps

USER api

ENTRYPOINT ["/code/app.py"]
