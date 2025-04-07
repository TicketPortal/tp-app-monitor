from flask import Flask, Response
import requests
import time
import threading
import json
import os

CONFIG_PATH = "/app/urls.json"
INTERVAL = 15

metrics = {}
urls = []

def load_urls():
    global urls
    try:
        with open(CONFIG_PATH) as f:
            urls = json.load(f)
    except Exception as e:
        print(f"Failed to load URLs: {e}")
        urls = []

def fetch_data():
    while True:
        load_urls()
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                data = response.json()
                info = data.get("info", {})
                rps = info.get("RPStotals", {})
                instance = info.get("instance", url)

                metrics[instance] = {
                    "workers": rps.get("workers", 0),
                    "rolingAvgRPS": rps.get("rolingAvgRPS", 0),
                    "RPS": rps.get("RPS", 0)
                }
            except Exception as e:
                print(f"Error fetching {url}: {e}")
        time.sleep(INTERVAL)

app = Flask(__name__)

@app.route("/metrics")
def get_metrics():
    output = []
    for instance, values in metrics.items():
        for key, val in values.items():
            output.append(f'# HELP json_{key} {key} from source instance')
            output.append(f'# TYPE json_{key} gauge')
            output.append(f'json_{key}{{instance="{instance}"}} {val}')
    return Response("\n".join(output), mimetype="text/plain")

if __name__ == "__main__":
    threading.Thread(target=fetch_data, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)