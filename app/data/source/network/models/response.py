from pydantic import BaseModel, Field

from app.data.models.models import Device


class DeviceResponse(BaseModel):
    id: int = Field(alias='id')
    type: int = Field(alias='type')
    udid: str = Field(alias='udid')
    account_id: int = Field(alias='accountId')
    location_id: int = Field(alias='locationId')

    def as_model(self) -> Device:
        return Device(
            id=self.id,
            udid=self.udid,
            account_id=self.account_id,
            location_id=self.location_id
        )
