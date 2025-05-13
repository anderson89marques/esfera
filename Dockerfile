FROM python:3.11-slim

RUN apt-get update && apt-get install gcc g++ make -y

WORKDIR /src

RUN pip install uv

COPY pyproject.toml .
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY entrypoint.sh .



RUN uv venv /src/venv && \
    . /src/venv/bin/activate && \
    uv sync -v

ENV PATH="/src/venv/bin:$PATH"
RUN chmod +x /src/entrypoint.sh

EXPOSE 8000
