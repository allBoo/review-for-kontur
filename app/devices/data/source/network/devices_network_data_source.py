from app.data.source.devices import DevicesHistoryDataSource
from app.data.source.network.api.devices_api import DevicesApi
from app.service.api.factory import Factory
from app.data.models.models import Device


class DevicesNetworkDataSource(DevicesHistoryDataSource):
    """
    CMS API Data Source for devices
    TODO: add ingestion for historical data
    """
    _preload_devices_count = 1000

    def __init__(self) -> None:
        api_client = Factory.get_cms_api_client()
        self._api_service = DevicesApi(api_client)

    async def get_devices(self) -> list[Device]:
        """
        Get all devices from CMS API
        """
        devices = await self._api_service.get_top_devices(self._preload_devices_count)
        return [device.as_model() for device in devices]

    async def get_device_by_udid(self, udid: str) -> Device | None:
        device = await self._api_service.get_device_by_udid(udid)
        return device.as_model() if device else None
