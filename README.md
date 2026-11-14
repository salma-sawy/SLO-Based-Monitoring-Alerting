# SLO-Based Monitoring & Alerting

A hands-on DevOps project that demonstrates how to monitor application health, measure service reliability, define Service Level Objectives (SLOs), and configure alerts using Prometheus, Grafana, and Alertmanager.

## Project Overview

This project implements a monitoring stack on an AWS EC2 instance using Docker Compose.

A simple Flask application exposes Prometheus metrics, while Prometheus collects application and infrastructure metrics. Grafana visualizes these metrics through a monitoring dashboard, and Alertmanager handles alerts when predefined conditions are met.

The goal is to understand how monitoring goes beyond collecting metrics to measuring service reliability and detecting potential incidents.

## Architecture

```text
                 Users
                   |
                   v
             Flask Application
                Port 8000
                   |
             /metrics endpoint
                   |
                   v
              Prometheus
                Port 9090
              /         \
             v           v
      Node Exporter   Alertmanager
          :9100          :9093
             |
             v
       Linux Metrics

              Grafana
               :3000
                 |
                 v
          Monitoring Dashboard
```

All services run as Docker containers on an AWS EC2 instance and communicate through the Docker Compose network.

## Technologies Used

- **AWS EC2:** Cloud infrastructure hosting the monitoring stack.
- **Linux (Ubuntu):** Server operating system.
- **Docker:** Containerization.
- **Docker Compose:** Multi-container application management.
- **Python / Flask:** Demo application exposing application metrics.
- **Prometheus:** Metrics collection and alert rule evaluation.
- **Node Exporter:** Linux infrastructure metrics collection.
- **Grafana:** Metrics visualization and dashboards.
- **Alertmanager:** Alert management and routing.

## Monitoring Metrics

The Grafana dashboard includes the following panels:

| Panel | Description |
|---|---|
| Application Availability | Percentage of requests that did not return HTTP 5xx responses |
| HTTP Error Rate | Percentage of HTTP 5xx responses |
| CPU Usage | Linux CPU utilization |
| Request Latency (p95) | 95th percentile of HTTP request duration |

## SLIs and SLOs

A Service Level Indicator (SLI) is a measurement of service performance.

A Service Level Objective (SLO) is the target value for that measurement.

This project uses the following example objectives:

| SLI | SLO Target |
|---|---|
| Application Availability | ≥ 99.9% |
| HTTP Error Rate | ≤ 0.1% |
| p95 Request Latency | ≤ 500 ms |
| CPU Usage | Below 80% (infrastructure threshold) |

**Note:** CPU usage is an infrastructure monitoring threshold, not a user-facing SLI.

## Error Budget

An Error Budget represents the amount of unreliability allowed by an SLO.

For a 99.9% availability objective:

- Allowed error rate: 0.1%
- For 1,000,000 eligible requests, the error budget is 1,000 failed requests.

The error budget helps determine whether the service is meeting its reliability objective.

## Alerting

Prometheus evaluates alert rules to detect potential problems.

The project includes alerts for:

- **HighCPUUsage:** Triggered when CPU usage exceeds 80% for 2 minutes.
- **ApplicationDown:** Triggered when Prometheus cannot scrape the application for 1 minute.
- **HighErrorRate:** Triggered when the HTTP 5xx error rate exceeds 0.1% for 2 minutes.

Alertmanager receives and manages the alerts.

## Failure Simulation

The Flask application includes endpoints for testing:

| Endpoint | Purpose |
|---|---|
| `/` | Application home |
| `/health` | Successful health check |
| `/fail` | Simulates an HTTP 500 error |
| `/metrics` | Exposes Prometheus metrics |

### Test Application Availability

Generate successful requests:

```bash
for i in {1..100}; do
  curl -s http://localhost:8000/health > /dev/null
done
```

Generate failed requests:

```bash
for i in {1..100}; do
  curl -s http://localhost:8000/fail > /dev/null
  sleep 0.2
done
```

The Availability and HTTP Error Rate panels should reflect the generated traffic over the configured five-minute observation window.

### Test Application Down Alert

Stop the application:

```bash
docker compose stop app
```

Prometheus should detect that the application target is down, triggering the `ApplicationDown` alert after its configured duration.

Restore the application:

```bash
docker compose start app
```

The target should become healthy again, and the alert should resolve.

## Project Structure

```text
SLO-Based-Monitoring-Alerting/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── prometheus/
│   └── prometheus.yml
│
├── rules/
│   └── alerts.yml
│
├── alertmanager/
│   └── alertmanager.yml
│
│── screanshots/
│   └── monitoring*.png
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Deployment

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/SLO-Based-Monitoring-Alerting.git

cd SLO-Based-Monitoring-Alerting
```

Start the monitoring stack:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

View service logs:

```bash
docker compose logs -f
```

## Accessing the Services

| Service | Address |
|---|---|
| Grafana | `http://EC2_PUBLIC_IP:3000` |
| Application | `http://localhost:8000` on EC2 |
| Prometheus | `http://localhost:9090` on EC2 |
| Alertmanager | `http://localhost:9093` on EC2 |

Prometheus and Alertmanager are bound to localhost and can be accessed remotely through an SSH tunnel if needed.

## What I Learned

- Deploying and managing a multi-container monitoring stack using Docker Compose.
- Collecting application and Linux metrics with Prometheus.
- Writing PromQL queries for availability, error rates, CPU usage, and latency.
- Building Grafana dashboards.
- Understanding SLIs, SLOs, and Error Budgets.
- Configuring Prometheus alert rules.
- Managing alerts through Alertmanager.
- Simulating application failures and observing monitoring behavior.

---

**Project Focus:** DevOps | Cloud Monitoring | Observability | Reliability Engineering

**Status:** Hands-on project in progress.
