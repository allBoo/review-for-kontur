from typing import Any

import httpx


class ApiClient:
    def __init__(self, base_url: str, api_token: str | None = None, **kwargs) -> None:
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={'Authorization': f'Bearer {api_token}'} if api_token else None,
            **kwargs
        )

    async def get(self, path: str) -> Any:
        async with self.client as client:
            response = await client.get(path)
        return response.json()

    async def post(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        pass

    async def put(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        pass

    async def delete(self, path: str) -> dict[str, Any]:
        pass
