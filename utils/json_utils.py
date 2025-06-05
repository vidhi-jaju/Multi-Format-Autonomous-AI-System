import json

def load_json(input_bytes: bytes):
    try:
        return json.loads(input_bytes.decode('utf-8'))
    except Exception:
        return None 