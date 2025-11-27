from __future__ import annotations

import logging
import sys
from typing import Any, Dict, List

from .config import load_settings
from .ninja_client import NinjaClient
from .fresh_client import FreshserviceClient
from .mapping import map_ninja_asset_to_fresh


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


def run_sync() -> int:
    setup_logging()
    logger = logging.getLogger("ninja_freshservice_sync")

    try:
        settings = load_settings()
    except Exception as exc:
        logging.getLogger(__name__).error("Failed to load configuration: %s", exc)
        return 1

    logger.info("Starting NinjaOne → Freshservice sync (dry_run=%s)", settings.dry_run)

    ninja = NinjaClient(
        base_url=settings.ninja_base_url,
        api_key=settings.ninja_api_key,
    )
    fresh = FreshserviceClient(
        base_url=settings.fresh_base_url,
        api_key=settings.fresh_api_key,
    )

    created = 0
    updated = 0
    errors = 0

    try:
        assets: List[Dict[str, Any]] = ninja.fetch_assets()
    except Exception as exc:
        logger.error("Error fetching assets from NinjaOne: %s", exc)
        return 1

    logger.info("Fetched %d assets from NinjaOne", len(assets))

    for asset in assets:
        try:
            payload = map_ninja_asset_to_fresh(asset, settings)

            if settings.dry_run:
                logger.debug("DRY RUN: would upsert asset: %s", payload.get("name"))
                continue

            result = fresh.upsert_asset(payload)
            # Once upsert is implemented, decide if it was created vs updated.
            # For now just count as updated.
            updated += 1
            logger.debug("Upserted asset: %s", result)
        except Exception as exc:
            errors += 1
            logger.error(
                "Failed to process asset %s: %s",
                asset.get("id") or asset.get("hostname"),
                exc,
            )

    logger.info(
        "Sync complete: created=%d updated=%d errors=%d",
        created,
        updated,
        errors,
    )

    return 0 if errors == 0 else 2


if __name__ == "__main__":
    sys.exit(run_sync())
