from flask import Flask, Response, request, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUESTS = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['endpoint']
)

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.route('/')
def home():
    return "SLO Monitoring Lab is running!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/fail')
def fail():
    return "Simulated server error", 500

@app.route('/metrics')
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

@app.after_request
def record_metrics(response):
    if request.path != '/metrics':
        endpoint = request.endpoint or 'unknown'
        REQUESTS.labels(
            request.method,
            endpoint,
            str(response.status_code)
        ).inc()

        LATENCY.labels(endpoint).observe(
            time.time() - g.start_time
        )

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
