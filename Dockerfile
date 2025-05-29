FROM python:3.11

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./


RUN pip install --upgrade pip \
    && pip install poetry \
    && pip install celery \
    && poetry config virtualenvs.create false \
    && poetry add celery \
    && poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]