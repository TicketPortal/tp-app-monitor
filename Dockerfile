FROM python:3.10-slim AS builder

WORKDIR /app
COPY exporter.py urls.json start.sh prometheus.yml ./
RUN pip install flask requests && chmod +x start.sh

# Final image based on Prometheus
FROM prom/prometheus:latest

COPY --from=builder /app /app

WORKDIR /app

EXPOSE 8000 9090

ENTRYPOINT ["/app/start.sh"]