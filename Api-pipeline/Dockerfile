# ── Stage 1: instalar dependencias ──────────────────────────────────────────
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
# numpy<2.0 no requiere X86_V2 (AVX/SSE4.2) — compatible con CPUs viejos.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: imagen final ligera ─────────────────────────────────────────────
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar dependencias compiladas del stage anterior
COPY --from=builder /install /usr/local

# Copiar codigo de la aplicacion
COPY . .

# Crear directorios de datos con permisos correctos
RUN mkdir -p /data/data/raw /data/data/processed /data/data/results /data/outputs/reportes

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
