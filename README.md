# NinjaOne → Freshservice Asset Sync

Containerized one-shot job that syncs asset/server data from NinjaOne into Freshservice CMDB.

## Overview

Per run:

1. Authenticate to NinjaOne and pull assets.
2. Map NinjaOne asset fields into Freshservice asset/CI payloads.
3. Authenticate to Freshservice.
4. Upsert assets (create or update).
5. Log summary and exit.

Designed to be run by a scheduler (cron/systemd/Swarm/etc.).

## Requirements

- Python 3.11+ (for local dev)
- Docker (for containerized execution)

## Configuration

All configuration is via environment variables.

Required:

- `NINJAONE_BASE_URL`
- `NINJAONE_API_KEY`
- `FRESHSERVICE_BASE_URL`
- `FRESHSERVICE_API_KEY`

Optional:

- `ASSET_DEFAULT_LOCATION`
- `ASSET_SOURCE_TAG`
- `DRY_RUN` (`true`/`false`)

See `.env.example` for a template.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export NINJAONE_BASE_URL=...
export NINJAONE_API_KEY=...
export FRESHSERVICE_BASE_URL=...
export FRESHSERVICE_API_KEY=...

python -m src.main
```

## Docker

Build:

```bash
docker build -t ninja-fs-sync .
```

Run:

```bash
docker run --rm \
  --env-file /opt/ninja-fs-sync/env \
  ninja-fs-sync:latest
```

## Scheduling

Example cron job (nightly at 02:00):

```
0 2 * * * docker run --rm \
  --env-file /opt/ninja-fs-sync/env \
  ninja-fs-sync:latest >> /var/log/ninja-fs-sync.log 2>&1
```

## Next steps

- Implement real NinjaOne asset fetching (`src/ninja_client.py`).
- Implement Freshservice asset lookup and upsert logic (`src/fresh_client.py`).
- Flesh out mapping for hostname, OS, IPs, serial, location, tags (`src/mapping.py`).
- Add tests and better error handling/retry behavior.
