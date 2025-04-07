FROM python:3.10-slim

WORKDIR /app

COPY exporter.py prometheus.yml ./
RUN pip install flask requests

# Also copy prometheus.yml to a shared volume path
RUN mkdir -p /shared && cp prometheus.yml /shared/prometheus.yml

EXPOSE 8000

CMD ["python", "exporter.py"]