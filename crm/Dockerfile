FROM python:3.8

WORKDIR /app

COPY src /app/src/
COPY tests /app/test/

RUN pip install poetry

COPY ["init_db_data.py",".env","poetry.lock","pyproject.toml","wsgi.py","/app/"]

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

CMD ["uwsgi", "--http", "0.0.0.0:8000", "--master", "-p", "4", "-w", "wsgi:app"]
