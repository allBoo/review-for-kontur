from datetime import date

from app.data.models.models import Device
from app.data.source.network.devices_network_data_source import DevicesNetworkDataSource


class DevicesHistoryRepository:
    """
    Retrieves the historical state of devices.
    TODO: implement the actual history retrieval
    """

    def __init__(self) -> None:
        self._devices: dict[str, Device | None] = {}

    async def preload_devices(self) -> None:
        devices = await DevicesNetworkDataSource.get_devices()
        for device in devices:
            self._devices[device.udid] = device

    async def find_device(self, udid: str, date: date) -> Device | None:
        if udid not in self._devices:
            device = await DevicesNetworkDataSource.get_device_by_udid(udid)
            self._devices[udid] = device

        return self._devices.get(udid)
