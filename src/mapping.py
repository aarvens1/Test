from __future__ import annotations

from typing import Any, Dict

from .config import Settings


def map_ninja_asset_to_fresh(
    ninja_asset: Dict[str, Any],
    settings: Settings,
) -> Dict[str, Any]:
    """
    Map a single NinjaOne asset record into a Freshservice asset payload.

    This is intentionally simple for now. As you refine the mapping, keep all
    transformations encapsulated here.
    """
    hostname = ninja_asset.get("hostname") or ninja_asset.get("name")
    serial = ninja_asset.get("serial_number") or ninja_asset.get("serial")

    payload: Dict[str, Any] = {
        # Example structure; adjust to Freshservice CMDB schema
        "name": hostname,
        "serial_number": serial,
        "description": f"Synced from NinjaOne",
        "impact": None,
        "used_by_id": None,
        "location": settings.asset_default_location,
        "custom_fields": {},
    }

    # Example: add a source tag
    if settings.asset_source_tag:
        # How tags are modeled in Freshservice may differ:
        payload.setdefault("tags", []).append(settings.asset_source_tag)

    # TODO: map OS, IPs, location, tags, etc. once you know NinjaOne schema
    return payload
