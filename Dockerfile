FROM python:3.10.4-alpine

ENV POETRY_VERSION=1.1.13 \
    APP_ENVIRONMENT='production'

RUN apk update && apk add gcc libc-dev libffi-dev
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /tmp
COPY poetry.lock pyproject.toml /tmp/

RUN poetry config virtualenvs.create false \
    && poetry install  $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

RUN python -c "import nltk;nltk.download('punkt')"

COPY . /data/app
WORKDIR /data/app

CMD ["gunicorn", "levatas_indexer:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8000"]
