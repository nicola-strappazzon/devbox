import time

from uptime_kuma_api import MonitorType, UptimeKumaApi

URL = "http://uptime-kuma:3001"
# Kuma requires a user to exist even with auth disabled (see set_settings below)
USER = "admin"
PASSWORD = "admin123"

PORT = MonitorType.PORT
HTTP = MonitorType.HTTP

# (name, type, target, port) — HTTP targets are URLs, PORT targets are hostnames
MONITORS = [
    ("Homer", HTTP, "http://homer:8080", None),
    ("MongoDB", PORT, "mongo", 27017),
    ("ClickHouse", HTTP, "http://clickhouse:8123/ping", None),
    ("Redis", PORT, "redis", 6379),
    ("Dozzle", HTTP, "http://dozzle:8080", None),
    ("PostgreSQL", PORT, "postgres", 5432),
    ("pgAdmin", HTTP, "http://pgadmin:80/misc/ping", None),
    ("Redis Insight", HTTP, "http://redisinsight:5540", None),
    ("Redpanda (Kafka)", PORT, "redpanda", 9092),
    ("Redpanda (Admin)", HTTP, "http://redpanda:9644/v1/status/ready", None),
    ("Redpanda Console", HTTP, "http://redpanda-console:8080", None),
    ("MySQL Primary", PORT, "mysql-primary", 3306),
    ("MySQL Replica", PORT, "mysql-replica", 3306),
    ("OTel Collector (HTTP)", PORT, "otel-collector", 4318),
    ("OTel Collector (gRPC)", PORT, "otel-collector", 4317),
    ("Prometheus", HTTP, "http://prometheus:9090/-/healthy", None),
    ("Grafana", HTTP, "http://grafana:3000/api/health", None),
    ("Redis Exporter", HTTP, "http://redis-exporter:9121/metrics", None),
    ("MongoDB Exporter", HTTP, "http://mongodb-exporter:9216/metrics", None),
    ("MySQL Exporter", HTTP, "http://mysql-exporter:9104/metrics", None),
    ("Node Exporter", HTTP, "http://node-exporter:9100/metrics", None),
]


def connect():
    for _ in range(30):
        try:
            return UptimeKumaApi(URL, timeout=60)
        except Exception:
            time.sleep(2)
    raise SystemExit("uptime-kuma not reachable")


api = connect()

if api.need_setup():
    api.setup(USER, PASSWORD)
    print("admin user created")

api.login(USER, PASSWORD)

# Local env: no login screen
api.set_settings(password=PASSWORD, disableAuth=True)

existing = {m["name"] for m in api.get_monitors()}
for name, mtype, target, port in MONITORS:
    if name in existing:
        continue
    kwargs = {"type": mtype, "name": name, "interval": 30, "maxretries": 2}
    if mtype == PORT:
        kwargs.update(hostname=target, port=port)
    else:
        kwargs.update(url=target)
    api.add_monitor(**kwargs)
    print(f"added {name}")

api.disconnect()
