FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY q_shield/ ./q_shield/
COPY vulnerable_sample.py ./

RUN pip install --no-cache-dir .

EXPOSE 8001

CMD ["uvicorn", "q_shield.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
