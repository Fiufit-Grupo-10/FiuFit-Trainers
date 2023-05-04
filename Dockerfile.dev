FROM python:3.10 as python-base

RUN mkdir app

WORKDIR /app

COPY /pyproject.toml /app

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80", "--reload"]
