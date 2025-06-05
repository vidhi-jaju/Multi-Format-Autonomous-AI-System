from typing import Dict, Any
from pydantic import BaseModel, ValidationError
from utils.json_utils import load_json

class WebhookSchema(BaseModel):
    event: str
    data: dict
    timestamp: str

def process_json(input_bytes: bytes) -> Dict[str, Any]:
    try:
        data = load_json(input_bytes)
        if data is None:
            raise ValueError('Invalid JSON')
        result = WebhookSchema(**data)
        return {'valid': True, 'data': result.dict(), 'anomalies': []}
    except ValidationError as ve:
        return {'valid': False, 'anomalies': ve.errors()}
    except Exception as e:
        return {'valid': False, 'anomalies': [str(e)]} 