FROM python:3.14-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install poetry and dependencies directly (no venv)
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Copy application code
COPY . .

CMD ["python", "main.py"]