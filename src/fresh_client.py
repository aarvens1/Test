from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class FreshserviceClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = session or requests.Session()
        # Freshservice typically uses API key as basic auth username with X as password
        self.session.auth = (self.api_key, "X")
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def upsert_asset(self, asset_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update an asset in Freshservice.

        Exact logic depends on how you identify uniqueness (e.g., serial number,
        hostname, custom field). For now this is a stub.
        """
        identifier = asset_payload.get("name") or asset_payload.get("display_name")
        logger.debug("Upserting asset in Freshservice: %s", identifier)

        # Placeholder: decide on lookup key and implement:
        # 1) GET existing asset by key
        # 2) POST or PUT accordingly

        # resp = self.session.post(self._url("/cmdb/items"), json=asset_payload)
        # resp.raise_for_status()
        # return resp.json()
        return {}
