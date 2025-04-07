# tp-app-monitor

✅ Features

•	Reads a list of external URLs from a JSON file (volume-mounted from host).
•	Dynamically supports any number of sources.
•	Extracts and exposes the following Prometheus metrics per info->instance:
•	workers
•	rolingAvgRPS
•	RPS

## urls.json

```
[
  "https://o2arena.tpapp.cz/probe/services",
  "https://example.com/another-instance"
]
```

## docker-compose.yaml

```
version: '3'

services:
  exporter:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./urls.json:/config/urls.json
    environment:
      - URLS_FILE=/config/urls.json

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

## grafana queries

```
json_RPS{instance="o2arena-1"}
json_rolingAvgRPS{instance="o2arena-1"}
json_workers{instance="o2arena-1"}
```