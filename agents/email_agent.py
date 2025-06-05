from textblob import TextBlob
from utils.email_utils import extract_email_fields

def analyze_tone(email_text: str) -> str:
    blob = TextBlob(email_text)
    polarity = blob.sentiment.polarity
    if polarity < -0.3:
        return 'angry'
    elif polarity > 0.3:
        return 'polite'
    # Heuristic for threatening/escalation
    import re
    if re.search(r'escalate|legal|lawsuit|threat|compensation', email_text, re.I):
        return 'threatening'
    return 'neutral'

def process_email(input_bytes: bytes) -> dict:
    email_text = input_bytes.decode(errors='ignore')
    fields = extract_email_fields(email_text)
    tone = analyze_tone(email_text)
    action = 'log_and_close'
    if tone in ['angry', 'threatening'] or fields['urgency'] == 'high':
        action = 'escalate_to_crm'
    return {**fields, 'tone': tone, 'action': action} 