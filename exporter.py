from flask import Flask, Response
import requests
import time
import threading

CONFIG_URL = "https://instances.tpapp.cz/config.json"
INTERVAL = 15

metrics = {}
sources = []

def load_config():
    global sources
    try:
        response = requests.get(CONFIG_URL, timeout=10)
        config = response.json()
        sources = [
            {
                "name": item["name"],
                "url": f"{item['api'].rstrip('/')}/probe/services"
            }
            for item in config if "api" in item and "name" in item
        ]
        print(f"Loaded {len(sources)} sources")
    except Exception as e:
        print(f"Failed to load config from {CONFIG_URL}: {e}")
        sources = []

def fetch_data():
    while True:
        load_config()
        for source in sources:
            try:
                resp = requests.get(source["url"], timeout=10)
                data = resp.json()
                info = data.get("info", {})
                rps = info.get("RPStotals", {})
                name = source["name"]

                metrics[name] = {
                    "workers": rps.get("workers", 0),
                    "rolingAvgRPS": rps.get("rolingAvgRPS", 0),
                    "RPS": rps.get("RPS", 0)
                }
            except Exception as e:
                print(f"Error fetching {source['url']}: {e}")
        time.sleep(INTERVAL)

app = Flask(__name__)

@app.route("/metrics")
def get_metrics():
    output = []
    for instance, values in metrics.items():
        for key, val in values.items():
            output.append(f'# HELP json_{key} {key} from instance')
            output.append(f'# TYPE json_{key} gauge')
            output.append(f'json_{key}{{instance="{instance}"}} {val}')
    return Response("\n".join(output), mimetype="text/plain")

if __name__ == "__main__":
    threading.Thread(target=fetch_data, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)