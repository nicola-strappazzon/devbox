# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A local development stack managed via Docker Compose. No application code — only infrastructure configuration.

## Key commands

```bash
docker compose up -d                    # start all services
docker compose up -d --build <service>  # rebuild and start a specific service (e.g. mysql-replica)
docker compose down                     # stop all
docker compose down -v                  # stop and wipe all volumes (destructive)
docker compose logs -f <service>        # tail logs
```

```bash
./watch-ip.sh                           # announce devbox.local on the LAN via mDNS (run in a terminal)
```

## Architecture

All services share a single `docker-compose.yml`. Config files are mounted as volumes — no images are built except `mysql-replica`.

**MySQL replication** is the only stateful relationship between services:
- `mysql-primary` (3306) runs stock `mysql:8.4` with GTID enabled via `mysql/primary/my.cnf` and creates the `replicator` user on first boot via `mysql/primary/init.sql`.
- `mysql-replica` (3307) uses a custom image (`mysql/replica/Dockerfile`) whose entrypoint waits for both instances to be healthy, then runs `CHANGE REPLICATION SOURCE TO ... GET_SOURCE_PUBLIC_KEY=1` to handle `caching_sha2_password` without SSL. It is read-only.

**Observability pipeline**: apps → OTel Collector (4317/4318) → Prometheus (scrapes :8889) → Grafana (3000). The Prometheus datasource is pre-provisioned via `grafana/provisioning/datasources/prometheus.yaml`.

**DNS**: `watch-ip.sh` uses `dns-sd -P` (macOS native mDNS) to announce `devbox.local` → current `en0` IP. No hostname change required. Re-registers automatically when IP changes.

## Caveats

- `mysql-replica` image must be rebuilt after changes to `mysql/replica/`: `docker compose up -d --build mysql-replica`
- MySQL init scripts in `docker-entrypoint-initdb.d/` only run on first boot (empty volume). To re-run them: `docker compose down -v && docker compose up -d`
- `watch-ip.sh` must run on the macOS host — avahi in Docker Desktop cannot reach the real LAN due to VM isolation.
