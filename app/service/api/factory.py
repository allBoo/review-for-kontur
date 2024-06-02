import typing

from .client import ApiClient
from app.config import Config


class Factory:

    _clients: dict[str, ApiClient] = {}

    @classmethod
    def _get_api_client(cls, base_url: str, api_token: str) -> ApiClient:
        if base_url in cls._clients:
            return cls._clients[base_url]

        cls._clients[base_url] = ApiClient(
            base_url=base_url,
            api_token=api_token,
        )

        return cls._clients[base_url]

    @classmethod
    def get_cms_api_client(cls) -> ApiClient:
        return cls._get_api_client(
            base_url=Config.CMS_API_BASE_URL,
            api_token=Config.CMS_API_TOKEN,
        )
