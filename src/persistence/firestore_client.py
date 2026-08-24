"""
Cresca AI — Firestore Persistence & Audit Ledger Client Module
Manages persistent state for autonomous runs and action plans in Google Cloud Firestore
with automatic graceful fallback to local storage during local test runs.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from src.config import GCP_PROJECT_ID, FIRESTORE_DATABASE, BASE_DIR

LOCAL_STORE_DIR = BASE_DIR / "data" / "firestore_local_store"
LOCAL_STORE_DIR.mkdir(parents=True, exist_ok=True)


class FirestoreManager:
    """
    Handles Google Cloud Firestore state persistence and audit ledger transactions.
    """

    RUNS_COLLECTION = "cresca_runs"
    PLANS_COLLECTION = "cresca_action_plans"

    def __init__(self, project_id: str = GCP_PROJECT_ID):
        self.project_id = project_id
        self.client = None
        self.is_live_firestore = False

        # Attempt to initialize Google Cloud Firestore client
        try:
            from google.cloud import firestore
            self.client = firestore.Client(project=self.project_id, database=FIRESTORE_DATABASE)
            # Test connection
            self.client.collections()
            self.is_live_firestore = True
            print(f"[FirestoreManager] Successfully connected to live Google Cloud Firestore ({self.project_id})")
        except Exception as e:
            print(f"[FirestoreManager] Live Firestore connection unavailable ({str(e)}). Operating in Hybrid Local Persistent Mode.")
            self.is_live_firestore = False

    def save_agent_run(self, execution_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Persists an autonomous agent run record into `cresca_runs`.
        """
        run_id = execution_payload["run_id"]
        run_doc = {
            "run_id": run_id,
            "timestamp": execution_payload.get("timestamp", datetime.now(timezone.utc).isoformat()),
            "trigger_source": execution_payload.get("trigger_source", "MANUAL"),
            "status": execution_payload.get("status", "COMPLETED_SUCCESS"),
            "execution_duration_sec": execution_payload.get("execution_duration_sec", 0),
            "anonymization_engine": execution_payload.get("privacy_guardrail_report", {}).get("guardrail_model", "Gemma 2"),
            "records_ingested": execution_payload.get("ingestion_metadata", {}).get("total_districts_loaded", 0),
            "total_projected_stunting_cases_90d": execution_payload.get("statistical_summary", {}).get("poisson_forecasting", {}).get("total_projected_cases", 0),
            "allocated_budget_idr": execution_payload.get("logistics_optimization", {}).get("total_budget_utilized_idr", 0),
            "pca_explained_variance_pct": execution_payload.get("statistical_summary", {}).get("pca_analysis", {}).get("pc1_explained_variance_pct", 0),
            "pdf_report_path": execution_payload.get("pdf_report_path", ""),
            "execution_logs_count": len(execution_payload.get("execution_logs", [])),
        }

        if self.is_live_firestore and self.client:
            try:
                self.client.collection(self.RUNS_COLLECTION).document(run_id).set(run_doc)
                print(f"[FirestoreManager] Committed run {run_id} to live Firestore collection '{self.RUNS_COLLECTION}'")
            except Exception as e:
                print(f"[FirestoreManager] Warning: failed to write to live Firestore: {e}")

        # Always save local JSON copy for offline audit & Streamlit dashboard access
        local_run_file = LOCAL_STORE_DIR / f"{run_id}.json"
        with open(local_run_file, "w", encoding="utf-8") as f:
            json.dump(execution_payload, f, indent=2)

        return run_doc

    def get_latest_runs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieves recent autonomous execution runs.
        """
        runs = []
        if self.is_live_firestore and self.client:
            try:
                docs = (
                    self.client.collection(self.RUNS_COLLECTION)
                    .order_by("timestamp", direction="DESCENDING")
                    .limit(limit)
                    .stream()
                )
                for d in docs:
                    runs.append(d.to_dict())
                if runs:
                    return runs
            except Exception:
                pass

        # Fallback to local files
        json_files = sorted(LOCAL_STORE_DIR.glob("CRESCA-RUN-*.json"), reverse=True)[:limit]
        for f in json_files:
            try:
                with open(f, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    runs.append({
                        "run_id": data.get("run_id"),
                        "timestamp": data.get("timestamp"),
                        "trigger_source": data.get("trigger_source"),
                        "status": data.get("status"),
                        "execution_duration_sec": data.get("execution_duration_sec"),
                        "total_projected_stunting_cases_90d": data.get("statistical_summary", {}).get("poisson_forecasting", {}).get("total_projected_cases", 0),
                        "allocated_budget_idr": data.get("logistics_optimization", {}).get("total_budget_utilized_idr", 0),
                    })
            except Exception:
                continue

        return runs
