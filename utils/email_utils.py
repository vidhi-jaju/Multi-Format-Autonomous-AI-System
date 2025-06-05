import re

def extract_email_fields(email_text: str) -> dict:
    sender = None
    subject = None
    urgency = 'normal'
    issue = None
    sender_match = re.search(r'From: (.+)', email_text)
    if sender_match:
        sender = sender_match.group(1).strip()
    subject_match = re.search(r'Subject: (.+)', email_text)
    if subject_match:
        subject = subject_match.group(1).strip()
    if re.search(r'urgent|immediate|asap|important', email_text, re.I):
        urgency = 'high'
    issue_match = re.search(r'(?:issue|request|problem|complaint):? (.+)', email_text, re.I)
    if issue_match:
        issue = issue_match.group(1).strip()
    return {'sender': sender, 'subject': subject, 'urgency': urgency, 'issue': issue} 