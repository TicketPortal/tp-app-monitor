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
  "https://o2arena.tpapp.cz/probe/services"
]
```

## docker-compose.yaml

```
services:
  prometheus:
    image: spectado/tp-app-monitor
    volumes:
      - ./urls.json:/app/urls.json

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