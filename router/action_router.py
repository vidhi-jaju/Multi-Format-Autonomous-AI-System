import requests
import random
from datetime import datetime
from typing import Dict

def route_action(action_type: str, payload: dict) -> Dict:
    # Simulate endpoint mapping
    endpoint_map = {
        'escalate_to_crm': 'http://dummy.local/crm/escalate',
        'log_and_close': 'http://dummy.local/log/close',
        'risk_alert': 'http://dummy.local/risk_alert',
    }
    url = endpoint_map.get(action_type, 'http://dummy.local/other')
    # Simulate REST call (no real request, just fake response)
    # In real use: response = requests.post(url, json=payload)
    response = {
        'url': url,
        'payload': payload,
        'status_code': 200,
        'response': f"Simulated {action_type} at {datetime.utcnow().isoformat()} (id={random.randint(1000,9999)})"
    }
    # Log action (could be extended to write to memory store)
    print(f"[ActionRouter] {action_type} -> {url} | Payload: {payload}")
    print(f"[ActionRouter] Response: {response['response']}")
    return response 