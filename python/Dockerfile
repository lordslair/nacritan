FROM alpine:3.16

RUN adduser -h /code -u 1000 -D -H api

ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY --chown=api:api /python   /code

WORKDIR /code
ENV PATH="/code/.local/bin:${PATH}"

RUN apk update --no-cache \
    && apk add --no-cache \
        "libjpeg" \
        "python3" \
        "tzdata" \
    && apk add --no-cache --virtual .build-deps \
        "gcc" \
        "g++" \
        "jpeg-dev" \
        "libc-dev" \
        "libffi-dev" \
        "python3-dev" \
        "zlib-dev" \
    && su api -c \
        "python3 -m ensurepip --upgrade && \
        pip3 install --user -U -r requirements.txt && \
        rm requirements.* Dockerfile" \
    && apk del .build-deps

USER api

ENTRYPOINT ["/usr/bin/python3", "app.py"]
