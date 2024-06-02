from app.data.source.network.api.devices_api import DevicesApi
from app.service.api.factory import Factory
from app.data.models.models import Device


class DevicesNetworkDataSource:
    """
    CMS API Data Source for devices
    TODO: add ingestion for historical data
    """

    _preload_devices_count = 1000

    @classmethod
    async def get_devices(cls) -> list[Device]:
        """
        Get all devices from CMS API
        """
        api_client = Factory.get_cms_api_client()
        api_service = DevicesApi(api_client)
        devices = await api_service.get_top_devices(cls._preload_devices_count)
        return [device.as_model() for device in devices]

    @staticmethod
    async def get_device_by_udid(udid: str) -> Device | None:
        api_client = Factory.get_cms_api_client()
        api_service = DevicesApi(api_client)
        device = await api_service.get_device_by_udid(udid)
        return device.as_model() if device else None
