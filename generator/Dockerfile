FROM python:3.9-slim
WORKDIR /app
COPY generator/generator.py .
RUN pip install requests opentelemetry-sdk opentelemetry-exporter-otlp
CMD ["python", "generator.py"]
