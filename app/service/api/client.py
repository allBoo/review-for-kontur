import json
import httpx

from pydantic import BaseModel
from typing import TypeVar, Generic, Annotated


T = TypeVar('T')


class ApiClient:
    def __init__(self, base_url: str, api_token: str = None, **kwargs):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={'Authorization': f'Bearer {api_token}'},
            **kwargs
        )

    async def get(self, path: str) -> dict:
        async with self.client as client:
            response = await client.get(path)
        return response.json()

    async def find_one(self, path: str, type: T) -> T:
        pass

    async def find_all(self, path: str, type: T) -> list[T]:
        pass

    async def post(self, path: str, data: dict) -> dict:
        pass

    async def put(self, path: str, data: dict) -> dict:
        pass

    async def delete(self, path: str) -> dict:
        pass
