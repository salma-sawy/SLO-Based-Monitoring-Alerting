# SLI and SLO Definitions

## Service
Demo Web Application

## SLI 1: Availability
Definition:
Percentage of successful HTTP requests.

Formula:
Successful Requests / Total Requests * 100

## SLO 1: Availability
Target: 99.9%

## SLI 2: Error Rate
Definition:
Percentage of HTTP 5xx responses.

## SLO 2: Error Rate
Target: Less than 0.1%

## SLI 3: Latency
Definition:
95th percentile HTTP response time.

## SLO 3: Latency
Target: Less than 500ms

## Error Budget

SLO: 99.9%

Allowed failure ratio: 0.1%

For 1,000,000 eligible requests:
Allowed failed requests = 1,000
