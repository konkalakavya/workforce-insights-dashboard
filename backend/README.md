# AI-Powered Workforce Analytics - Backend

This folder contains only the Flask backend. It uses the project's existing
`data/` and `ml/` folders instead of creating duplicate copies.

## Expected project layout

```text
AI-Powered-Workforce-Analytics/
├── backend/
├── data/
│   ├── WA_Fn-UseC_-HR-Employee-Attrition.csv
│   └── workforce_processed.csv
├── ml/
└── frontend/
```

## Setup

From the project root:

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

Server:

```text
http://127.0.0.1:5000
```

Health check:

```text
GET /api/health
```

## API endpoints

### Dashboard

```text
GET /api/dashboard/
```

### Employees

```text
GET /api/employees/
GET /api/employees/?search=Sales
GET /api/employees/?department=Sales
GET /api/employees/?job_role=Sales Executive
GET /api/employees/top-performers
GET /api/employees/high-risk
```

### Analytics

```text
GET /api/analytics/overview
GET /api/analytics/performance
GET /api/analytics/salary
GET /api/analytics/attrition
GET /api/analytics/departments
GET /api/analytics/health
```

### ML prediction

```text
POST /api/predict/attrition
POST /api/predict/promotion
```

The attrition endpoint loads/trains the Random Forest model from the existing
ML/data setup and saves the generated model under `ml/saved_models/`.

The standard IBM HR Attrition dataset does not contain a validated promotion
target, so the promotion endpoint is explicitly a transparent readiness
heuristic rather than a supervised ML prediction.

### Chat

```text
POST /api/chat/
```

Example:

```json
{
  "question": "What is the attrition rate?"
}
```

## Important

If your dataset filename is different, change `DATA_FILE` in `config.py`.

The backend does not contain the dataset or duplicate ML folder.
