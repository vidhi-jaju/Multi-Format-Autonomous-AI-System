from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from typing import Optional
from agents.classifier_agent import classify
from agents.email_agent import process_email
from agents.json_agent import process_json
from agents.pdf_agent import process_pdf
from router.action_router import route_action
from memory.memory_store import (
    log_input, log_extracted_field, log_action, log_trace, get_all_logs, get_trace_by_trace_id
)

app = FastAPI(title="Multi-Format Autonomous AI System")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
    <head><title>Multi-Format AI System Upload</title></head>
    <body>
        <h2>Upload Input</h2>
        <form action="/upload/email" enctype="multipart/form-data" method="post">
            <h3>Email Upload</h3>
            <input name="file" type="file" accept=".eml,.txt,.msg" required />
            <button type="submit">Upload Email</button>
        </form>
        <form action="/upload/json" enctype="multipart/form-data" method="post">
            <h3>JSON Upload</h3>
            <input name="file" type="file" accept=".json" required />
            <button type="submit">Upload JSON</button>
        </form>
        <form action="/upload/pdf" enctype="multipart/form-data" method="post">
            <h3>PDF Upload</h3>
            <input name="file" type="file" accept=".pdf" required />
            <button type="submit">Upload PDF</button>
        </form>
        <p>Or use <a href="/docs">Swagger UI</a> for API testing.</p>
    </body>
    </html>
    """

# --- Upload Endpoints ---
@app.post("/upload/email")
async def upload_email(file: UploadFile = File(...)):
    input_bytes = await file.read()
    classification = classify(input_bytes, file.filename)
    input_id, trace_id = log_input('email', classification['intent'], input_metadata=classification)
    log_trace(input_id, 'classified', str(classification))
    agent_result = process_email(input_bytes)
    for k, v in agent_result.items():
        log_extracted_field(input_id, k, v)
    log_trace(input_id, 'email_agent', str(agent_result))
    action_result = route_action(agent_result['action'], agent_result)
    log_action(input_id, agent_result['action'], 'success', str(action_result))
    log_trace(input_id, 'action_router', str(action_result))
    return {"trace_id": trace_id, "classification": classification, "agent_result": agent_result, "action_result": action_result}

@app.post("/upload/json")
async def upload_json(file: UploadFile = File(...)):
    input_bytes = await file.read()
    classification = classify(input_bytes, file.filename)
    input_id, trace_id = log_input('json', classification['intent'], input_metadata=classification)
    log_trace(input_id, 'classified', str(classification))
    agent_result = process_json(input_bytes)
    for k, v in agent_result.items():
        log_extracted_field(input_id, k, v)
    log_trace(input_id, 'json_agent', str(agent_result))
    action_type = 'risk_alert' if not agent_result.get('valid', True) else 'log_and_close'
    action_result = route_action(action_type, agent_result)
    log_action(input_id, action_type, 'success', str(action_result))
    log_trace(input_id, 'action_router', str(action_result))
    return {"trace_id": trace_id, "classification": classification, "agent_result": agent_result, "action_result": action_result}

@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    input_bytes = await file.read()
    classification = classify(input_bytes, file.filename)
    input_id, trace_id = log_input('pdf', classification['intent'], input_metadata=classification)
    log_trace(input_id, 'classified', str(classification))
    agent_result = process_pdf(input_bytes)
    for k, v in agent_result['extracted'].items():
        log_extracted_field(input_id, k, v)
    log_trace(input_id, 'pdf_agent', str(agent_result))
    action_type = 'risk_alert' if 'invoice_total_gt_10000' in agent_result['flags'] or any(f.startswith('policy_mentions_') for f in agent_result['flags']) else 'log_and_close'
    action_result = route_action(action_type, agent_result)
    log_action(input_id, action_type, 'success', str(action_result))
    log_trace(input_id, 'action_router', str(action_result))
    return {"trace_id": trace_id, "classification": classification, "agent_result": agent_result, "action_result": action_result}

# --- Logs and Traces Endpoints ---
@app.get("/logs")
async def get_logs():
    logs = get_all_logs()
    return {"logs": logs}

@app.get("/traces/{trace_id}")
async def get_trace(trace_id: str):
    trace = get_trace_by_trace_id(trace_id)
    return {"trace_id": trace_id, "trace": trace} 