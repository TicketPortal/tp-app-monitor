FROM python:3.10-slim AS builder

# Set up exporter
WORKDIR /app
COPY exporter.py urls.json start.sh prometheus.yml ./
RUN pip install flask requests \
 && chmod +x start.sh

# Final image with Prometheus included
FROM prom/prometheus:latest

COPY --from=builder /app /app

WORKDIR /app

ENV URLS_FILE=/app/urls.json

EXPOSE 8000 9090

CMD ["./start.sh"]