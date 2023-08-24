FROM python:3.10

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        gcc \
        g++ \
        libffi-dev \
        musl-dev

ENV PYTHONIOENCODING=utf-8
WORKDIR /app

RUN adduser --system --group --home /home/app app && chown -R app:app /app

USER app
ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app requirements.txt .
RUN pip install --user -r requirements.txt && \
    rm requirements.txt

COPY --chown=app:app . .

ARG API_VERSION
ENV API_VERSION=$API_VERSION

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--proxy-headers", "--log-config", "config/logging.prod.ini"]
