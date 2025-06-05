# Multi-Format Autonomous AI System

## Overview
A multi-agent system that processes Email, JSON, and PDF inputs, classifies both format and business intent, routes to specialized agents, and dynamically chains follow-up actions based on extracted data (e.g., triggering an alert, generating a summary, flagging a risk). All steps are logged for traceability.

## Features
- **Classifier Agent:** Detects input format and business intent.
- **Email Agent:** Extracts sender, urgency, issue/request, and tone; triggers escalation or logs.
- **JSON Agent:** Validates schema, flags anomalies.
- **PDF Agent:** Extracts invoice/policy data, flags high-value or compliance risks.
- **Action Router:** Simulates REST calls for follow-up actions.
- **Shared Memory Store:** Logs all steps, fields, actions, and traces with unique trace IDs.
- **Simple UI:** Upload form at `/` and full API docs at `/docs`.
- **Dockerized:** Easy to run anywhere.

## Architecture
```mermaid
graph TD
    A[User Upload (Email/JSON/PDF)] --> B[Classifier Agent]
    B -->|Format+Intent| C1[Email Agent]
    B -->|Format+Intent| C2[JSON Agent]
    B -->|Format+Intent| C3[PDF Agent]
    C1 --> D[Action Router]
    C2 --> D
    C3 --> D
    D --> E[Simulated REST Action]
    B --> F[Memory Store]
    C1 --> F
    C2 --> F
    C3 --> F
    D --> F
    F --> G[Logs/Traces API]
```

## Setup
1. **Clone the repo**
2. **Install Docker** (or Python 3.10+ and pip)
3. **Build and run with Docker:**
   ```sh
   docker build -t multiagent-ai-system .
   docker run -p 8000:8000 multiagent-ai-system
   ```
   Or run locally:
   ```sh
   pip install -r requirements.txt
   uvicorn api.main:app --reload
   ```

## Usage
- Visit [http://localhost:8000/](http://localhost:8000/) for the upload UI
- Or use [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger API
- Upload sample files from `static/sample_inputs/`
- View logs at `/logs` and traces at `/traces/{trace_id}`

## Sample Inputs
- `static/sample_inputs/sample_email.eml`
- `static/sample_inputs/sample_webhook.json`
- `static/sample_inputs/sample_invoice.pdf` (replace with a real PDF for full test)

## Output Logs
- All actions, extracted fields, and traces are logged in SQLite (`memory_store.db`).
- Use `/logs` and `/traces/{trace_id}` to view processing history.

## Project Structure
```
project/
├── agents/
│   ├── classifier_agent.py
│   ├── email_agent.py
│   ├── json_agent.py
│   └── pdf_agent.py
├── api/
│   └── main.py
├── memory/
│   └── memory_store.py
├── router/
│   └── action_router.py
├── utils/
│   ├── pdf_utils.py
│   ├── email_utils.py
│   └── json_utils.py
├── static/
│   └── sample_inputs/
├── requirements.txt
├── Dockerfile
└── README.md
```

## Screenshots
Add screenshots of the UI, logs, and traces here.

## License
MIT 