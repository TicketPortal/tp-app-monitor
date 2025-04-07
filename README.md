# tp-app-monitor

✅ Features

- Reads a list of external URLs from a JSON file (volume-mounted from host).
- Dynamically supports any number of sources.
- Extracts and exposes the following Prometheus metrics per info->instance:
- workers
- rolingAvgRPS
- RPS

! depends on `https://instances.tpapp.cz/config.json` for source configuration.

## docker-compose.yaml

```
services:
  exporter:
    image: spectado/tp-app-monitor
    volumes:
      - prometheus-config:/shared

  prometheus:
    image: prom/prometheus
    command:
      - '--config.file=/shared/prometheus.yml'
    volumes:
      - prometheus-config:/shared

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"

volumes:
  prometheus-config:
```

## grafana queries

```
json_RPS{instance="o2arena"}
json_rolingAvgRPS{instance="o2arena"}
json_workers{instance="o2arena"}
```