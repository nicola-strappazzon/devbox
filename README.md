# Local Dev Stack

## Services

| Service | Port(s) | User | Password | Notes |
|---|---|---|---|---|
| Homer | 80 | — | — | `http://devbox.local` — dashboard con todos los servicios |
| MongoDB | 27017 | — | — | `mongodb://devbox.local:27017` |
| ClickHouse | 8123 (HTTP), 9000 (native) | `default` | `clickhouse` | `docker exec -it clickhouse clickhouse-client --password clickhouse` |
| Redis | 6379 | — | — | `redis://devbox.local:6379` |

| MySQL Primary | 3306 | `root` | `root` | `mysql -h devbox.local -P 3306 -u root -proot` |
| MySQL Replica | 3307 | `root` | `root` | `mysql -h devbox.local -P 3307 -u root -proot` — read-only |
| OTel Collector | 4317 (gRPC), 4318 (HTTP) | — | Bearer `OTEL_TOKEN` (from `.env`) | `OTEL_EXPORTER_OTLP_ENDPOINT=http://devbox.local:4317` + `OTEL_EXPORTER_OTLP_HEADERS="authorization=Bearer $OTEL_TOKEN"` |
| Prometheus | 9090 | — | — | `http://devbox.local:9090` |
| Grafana | 3000 | `admin` | `grafana` | `http://devbox.local:3000` — Prometheus pre-configured |

## MySQL Replication

GTID-based replication. Primary → Replica (read-only). Replication user: `replicator` / `replicator`.

## DNS

`devbox.local` resolves to this machine's LAN IP via mDNS. Keep the watcher running in a terminal:

```bash
./watch-ip.sh
```

## Evitar sleep al cerrar la tapa (macOS)

```bash
caffeinate -i &                        # previene idle sleep, permite apagar pantalla (sesión actual)
sudo pmset -a disablesleep 1           # deshabilita sleep por cierre de tapa (requiere admin)
sudo pmset -a displaysleep 10          # apaga pantalla tras 10 min de inactividad (requiere admin)
```

Sin permisos de admin: **Amphetamine** (App Store, gratis) con la opción "Allow Display to Sleep".

## Commands

```bash
docker compose up -d       # start all
docker compose down        # stop all
docker compose down -v     # stop + delete all data
docker compose logs -f [service]
```
