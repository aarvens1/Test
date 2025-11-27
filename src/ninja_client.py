from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Optional

import requests

logger = logging.getLogger(__name__)


class NinjaClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
            }
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def fetch_assets(self) -> List[Dict[str, Any]]:
        """
        Fetch assets/servers from NinjaOne.

        Paging and filtering should be implemented here once API details are known.
        """
        logger.info("Fetching assets from NinjaOne")
        # Placeholder implementation
        # resp = self.session.get(self._url("/v2/devices"))
        # resp.raise_for_status()
        # data = resp.json()
        # return data.get("devices", [])
        return []
