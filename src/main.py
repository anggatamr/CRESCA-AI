"""
Cresca AI — FastAPI Cloud Run Microservice Entrypoint
Provides REST endpoints for:
1. /trigger-run : Invoked asynchronously by Google Cloud Scheduler / Pub/Sub
2. /latest-runs : Returns execution history and risk alerts
3. /reports/{run_id}.pdf : Serves compiled Action Plan PDF documents
4. /health : Liveness & Readiness probe for Cloud Run
"""

from pathlib import Path
from typing import Dict, Any
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.agent.orchestrator import CrescaAgentOrchestrator
from src.persistence.firestore_client import FirestoreManager
from src.config import REPORTS_DIR

app = FastAPI(
    title="Cresca AI — Autonomous Sentinel API",
    description="Asynchronous background API for demographic risk assessment and nutrition logistics dispatch.",
    version="1.0.0",
)

# Enable CORS for dashboard integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons
orchestrator = CrescaAgentOrchestrator()
firestore_mgr = FirestoreManager()


@app.get("/health", tags=["System"])
def health_check() -> Dict[str, Any]:
    """Cloud Run Liveness & Readiness probe."""
    return {
        "status": "HEALTHY",
        "service": "cresca-sentinel-api",
        "mode": "AUTONOMOUS_TASKMASTER",
        "firestore_connected": firestore_mgr.is_live_firestore,
    }


@app.post("/trigger-run", tags=["Autonomous Pipeline"])
def trigger_agent_run(trigger_source: str = "CLOUD_SCHEDULER_CRON") -> Dict[str, Any]:
    """
    Triggers an asynchronous autonomous pipeline cycle.
    Can be invoked by Google Cloud Scheduler HTTP Target.
    """
    try:
        execution_result = orchestrator.execute_autonomous_run(trigger_source=trigger_source)
        return {
            "status": "SUCCESS",
            "run_id": execution_result["run_id"],
            "execution_duration_sec": execution_result["execution_duration_sec"],
            "total_projected_cases": execution_result["statistical_summary"]["poisson_forecasting"]["total_projected_cases"],
            "budget_utilized_idr": execution_result["logistics_optimization"]["total_budget_utilized_idr"],
            "pdf_report_path": execution_result.get("pdf_report_path", ""),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Autonomous run failed: {str(e)}")


@app.get("/latest-runs", tags=["Persistence & Audit"])
def get_recent_runs(limit: int = 10):
    """Retrieves recent run audit logs."""
    runs = firestore_mgr.get_latest_runs(limit=limit)
    return {"count": len(runs), "runs": runs}


@app.get("/reports/{run_id}.pdf", tags=["Artifacts"])
def download_action_plan_pdf(run_id: str):
    """Serves compiled PDF action plans."""
    pdf_file = REPORTS_DIR / f"{run_id}.pdf"
    if not pdf_file.exists():
        raise HTTPException(status_code=404, detail="Requested PDF report not found.")
    return FileResponse(
        path=pdf_file,
        filename=f"{run_id}.pdf",
        media_type="application/pdf",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
