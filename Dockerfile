# Stage 1: Build Native Probes
FROM ubuntu:22.04 AS native-builder
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    clang \
    gcc \
    make \
    libbpf-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY core/native/ core/native/
RUN cd core/native && make all

# Stage 2: Runtime Application Container
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    libbpf0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=native-builder /app/core/native/memory_inspector core/native/
COPY --from=native-builder /app/core/native/qshield_probe.bpf.o core/native/
COPY . .

# Generate static UI dashboard on boot
RUN python generate_dashboard.py

EXPOSE 8000
CMD ["uvicorn", "q_shield.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
