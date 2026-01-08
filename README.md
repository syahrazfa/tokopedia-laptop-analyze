# Tokopedia Laptop Market Intelligence Engine

Production-grade market intelligence system for tracking, analyzing, and alerting Tokopedia laptop price dynamics.

This system ingests live Tokopedia product data, normalizes it into a multi-layer analytical warehouse, computes momentum, detects price crashes, and dispatches alerts.

---

## Architecture

Layered data system:

bronze → silver → gold → dispatch

| Layer | Purpose |
|------|---------|
| bronze | Raw market ingestion |
| silver | Clean normalized product prices |
| gold | Momentum, alerts, and analytics |
| dispatch | Outbound alert delivery |

---

## Core Pipelines

| File | Role |
|-----|-----|
| tokopedia_json_sensor.py | Market ingestion |
| bronze_to_silver.py | Normalization |
| silver_to_gold.py | Aggregation |
| gold_price_momentum.py | Price delta engine |
| gold_price_alerts.py | Crash detection |
| alert_dispatcher.py | Alert delivery |

---

## Requirements

- Python 3.11+
- PostgreSQL 14+
- psycopg2
- requests
- python-dotenv

---

## Environment

Create `.env`:

---

# LICENSE

Apache License 2.0

---

# 🌟 About Me
Hi, im Raz,

I am building my career at the intersection of data engineering, financial logic, and operator decision systems.

My work focuses on freezing real business reality into decision-grade data structures that support capital allocation, margin optimization, and risk visibility — not just dashboards and reports.

This repository is part of a long-term effort to move from technical data roles into operator and investment-facing positions, where data is used to change outcomes, not simply describe them.
