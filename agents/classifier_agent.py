import re
import json
from typing import Optional

# Few-shot examples for intent detection
FEW_SHOT_EXAMPLES = [
    {"text": "Request for quotation for 100 units", "intent": "RFQ"},
    {"text": "We have a complaint about your service", "intent": "Complaint"},
    {"text": "Invoice #12345 for your recent purchase", "intent": "Invoice"},
    {"text": "As per GDPR regulation, ...", "intent": "Regulation"},
    {"text": "This transaction looks suspicious and may be fraud", "intent": "Fraud Risk"},
]

INTENT_KEYWORDS = {
    "RFQ": ["request for quotation", "rfq", "quote request"],
    "Complaint": ["complaint", "not satisfied", "issue", "problem"],
    "Invoice": ["invoice", "amount due", "bill", "payment due"],
    "Regulation": ["regulation", "gdpr", "fda", "compliance"],
    "Fraud Risk": ["fraud", "suspicious", "risk", "alert"],
}


def detect_format(input_bytes: bytes, filename: Optional[str] = None) -> str:
    if filename:
        ext = filename.lower().split('.')[-1]
        if ext == 'pdf':
            return 'PDF'
        elif ext == 'json':
            return 'JSON'
        elif ext in ['eml', 'msg', 'txt']:
            return 'Email'
    # Fallback: try to guess from content
    try:
        json.loads(input_bytes.decode('utf-8'))
        return 'JSON'
    except Exception:
        pass
    if b'%PDF' in input_bytes[:10]:
        return 'PDF'
    # Heuristic: look for email headers
    if b'From:' in input_bytes[:100] and b'Subject:' in input_bytes[:200]:
        return 'Email'
    return 'Unknown'

def detect_intent(text: str) -> str:
    text_lower = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return intent
    # Fallback: few-shot similarity (very simple)
    for ex in FEW_SHOT_EXAMPLES:
        if ex["text"].lower() in text_lower:
            return ex["intent"]
    return 'Unknown'

def classify(input_bytes: bytes, filename: Optional[str] = None) -> dict:
    fmt = detect_format(input_bytes, filename)
    # Try to extract text for intent detection
    if fmt == 'JSON':
        try:
            data = json.loads(input_bytes.decode('utf-8'))
            text = json.dumps(data)
        except Exception:
            text = input_bytes.decode(errors='ignore')
    elif fmt == 'PDF':
        text = '[PDF content not extracted here]'
    else:
        text = input_bytes.decode(errors='ignore')
    intent = detect_intent(text)
    routing_metadata = {"format": fmt, "intent": intent}
    return {"format": fmt, "intent": intent, "routing_metadata": routing_metadata} 