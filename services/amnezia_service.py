from datetime import datetime, timedelta
from typing import Any

import httpx
import secrets
import string

from config import (
    AMNEZIA_API_KEY,
    AMNEZIA_API_URL,
    DEFAULT_PROTOCOL,
)
from models.vpn_client import VPNClient


class AmneziaAPIError(Exception):
    """Ошибка при работе с API Amnezia."""


class AmneziaService:

    def __init__(self):
        self.base_url = AMNEZIA_API_URL.rstrip("/")

        self.headers = {
            "x-api-key": AMNEZIA_API_KEY,
            "Content-Type": "application/json",
        }

    def generate_client_name(self) -> str:
        alphabet = string.ascii_uppercase + string.digits

        random_part = "".join(
            secrets.choice(alphabet)
            for _ in range(6)
        )

        return f"HSVPN-{random_part}"

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Any:

        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=30
        ) as client:

            response = await client.request(
                method,
                endpoint,
                **kwargs
            )

        if response.status_code >= 400:
            raise AmneziaAPIError(
                f"{response.status_code}: {response.text}"
            )

        if not response.content:
            return None

        return response.json()

    # ---------------------------------------------------
    # Проверка соединения
    # ---------------------------------------------------

    async def healthcheck(self) -> bool:

        try:
            await self.get_clients()
            return True

        except Exception:
            return False

    # ---------------------------------------------------
    # Получить список клиентов
    # ---------------------------------------------------

    async def get_clients(self) -> list[dict]:

        return await self._request(
            "GET",
            "/clients"
        )

    # ---------------------------------------------------
    # Получить клиента
    # ---------------------------------------------------

    async def get_client(
        self,
        client_id: str
    ) -> dict:

        return await self._request(
            "GET",
            f"/clients/{client_id}"
        )

    # ---------------------------------------------------
    # Создать клиента
    # ---------------------------------------------------

    async def create_client(
        self,
        days: int,
        protocol: str = DEFAULT_PROTOCOL
    ) -> VPNClient:

        expires = int(
            (
                datetime.utcnow()
                + timedelta(days=days)
            ).timestamp()
        )

        client_name = self.generate_client_name()

        payload = {
            "clientName": client_name,
            "protocol": protocol,
            "expiresAt": expires
        }

        result = await self._request(
            "POST",
            "/clients",
            json=payload
        )

        client = result["client"]

        return VPNClient(
            id=client["id"],
            client_name=client.get("clientName", client_name),
            protocol=client["protocol"],
            config=client.get("config"),
            expires_at=client.get("expiresAt")
        )

    # ---------------------------------------------------
    # Удалить клиента
    # ---------------------------------------------------

    async def delete_client(
        self,
        client_id: str
    ) -> dict:

        return await self._request(
            "DELETE",
            f"/clients/{client_id}"
        )

    # ---------------------------------------------------
    # Продлить подписку
    # ---------------------------------------------------

    async def update_expiration(
        self,
        client_id: str,
        days: int
    ) -> dict:

        expires = int(
            (
                datetime.utcnow()
                + timedelta(days=days)
            ).timestamp()
        )

        payload = {
            "expiresAt": expires
        }

        return await self._request(
            "PATCH",
            f"/clients/{client_id}",
            json=payload
        )

amnezia = AmneziaService()
