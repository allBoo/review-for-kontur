from app.data.source.network.models.response import DeviceResponse
from app.infrastructure.api.client import ApiClient


class DevicesApi:

    _base_path = '/api/public/devices/v0/'

    def __init__(self, client: ApiClient):
        self.client = client

    async def get_top_devices(self, limit: int) -> list[DeviceResponse]:
        """
        Get top N last active devices from CMS API
        """
        devices = await self.client.get(f'{self._base_path}history?sort=last_activity&page-size={limit}')
        assert devices is not None, 'Failed to get devices from CMS API'
        assert isinstance(devices, list), 'Unexpected response from CMS API'

        return [DeviceResponse(**device) for device in devices]

    async def get_device_by_udid(self, udid: str) -> DeviceResponse | None:
        """
        Get single device by its udid
        :param udid:
        :return:
        """
        device = await self.client.get(f'{self._base_path}history/{udid}/')
        if device:
            return DeviceResponse(**device)
        return None
