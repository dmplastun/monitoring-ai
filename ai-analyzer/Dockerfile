FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*
RUN pip install prometheus-api-client
RUN pip install prometheus_client
RUN pip install requests
COPY . .
CMD ["python", "app.py"]
