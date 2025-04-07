#!/bin/bash

# Start the Python exporter in the background
python3 exporter.py &

# Start Prometheus with embedded config
/prometheus \
  --config.file=/app/prometheus.yml \
  --web.listen-address=":9090"