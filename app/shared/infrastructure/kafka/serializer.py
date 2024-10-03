from pydantic import BaseModel
import json


class KafkaDataSerializer:
    @staticmethod
    def serialize(data: BaseModel) -> str:
        return json.dumps(data.model_dump(mode='json'))

    @staticmethod
    def deserialize(data: str, model_class: type[BaseModel]) -> BaseModel:
        return model_class.parse_raw(data)
