FROM python:3.10-slim

WORKDIR /app

COPY exporter.py .
COPY prometheus.yml /etc/prometheus/prometheus.yml

RUN pip install flask requests

EXPOSE 8000

CMD ["python", "exporter.py"]