import re
from typing import Dict, Any
from utils.pdf_utils import extract_pdf_text

def process_pdf(input_bytes: bytes) -> Dict[str, Any]:
    text = extract_pdf_text(input_bytes)
    result = {'flags': [], 'extracted': {}}
    # Invoice total detection
    total_match = re.search(r'Total\s*[:=]?\s*\$?([\d,]+\.?\d*)', text, re.I)
    if total_match:
        total = float(total_match.group(1).replace(',', ''))
        result['extracted']['invoice_total'] = total
        if total > 10000:
            result['flags'].append('invoice_total_gt_10000')
    # Policy keyword detection
    for keyword in ['GDPR', 'FDA', 'HIPAA', 'PCI']:
        if keyword.lower() in text.lower():
            result['flags'].append(f'policy_mentions_{keyword.lower()}')
    result['extracted']['text_snippet'] = text[:500]
    return result 