from abc import ABC, abstractmethod

from ..models import Device


class DevicesHistoryDataSource(ABC):
    @abstractmethod
    async def get_devices(self) -> list[Device]:
        raise NotImplementedError

    @abstractmethod
    async def get_device_by_udid(self, udid: str) -> Device | None:
        raise NotImplementedError
