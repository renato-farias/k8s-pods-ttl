FROM python:3.10-alpine AS builder

ENV POETRY_VERSION=1.4.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME="/opt/poetry" \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

## install system deps
RUN python -m pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION" && poetry --version

## install python deps
RUN mkdir -p /build/app/source/
ADD ${PROJECT_NAME}/pyproject.toml /build/app/source/

WORKDIR /build/app/source
RUN poetry install --no-dev --no-interaction --no-ansi

WORKDIR /home/apps/app
RUN rm -rf /build

RUN adduser -D -s /bin/bash -h /home/apps apps

## copy app
ADD main.py pod_ttl.py /home/apps/app/

FROM scratch

COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

USER apps

COPY --from=builder --chown=apps:apps /usr/local/lib /usr/local/lib
COPY --from=builder --chown=apps:apps /usr/local/bin /usr/local/bin
COPY --from=builder --chown=apps:apps /usr/lib /usr/lib
COPY --from=builder --chown=apps:apps /lib /lib
COPY --from=builder --chown=apps:apps /home/apps/app /home/apps/app
WORKDIR /home/apps/app

ENTRYPOINT ["/usr/local/bin/python3"]

CMD ["-m", "kopf", "run", "main.py"]
