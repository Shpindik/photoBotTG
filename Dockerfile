FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY bot ./bot
COPY admin_backend ./admin_backend

FROM base AS bot
CMD ["python", "bot/main.py"]

FROM base AS admin
CMD ["uvicorn", "admin_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
