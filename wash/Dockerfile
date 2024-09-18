FROM python:3.9-slim
WORKDIR /app
COPY wash.py .
RUN pip install flask opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
CMD ["python", "wash.py"]
