"""
End-to-End Integration Test for CrescaAgentOrchestrator.
Validates that the complete autonomous agent loop executes seamlessly:
Ingestion -> Privacy Scrubbing -> Stats -> Logistics -> Gemini Reasoning -> PDF Generation -> Firestore Persistence.
"""

from pathlib import Path
import pytest
from src.agent.orchestrator import CrescaAgentOrchestrator


def test_autonomous_agent_execution_loop():
    orchestrator = CrescaAgentOrchestrator()
    result = orchestrator.execute_autonomous_run(trigger_source="INTEGRATION_TEST_RUNNER")

    # 1. Assertions on Execution Lifecycle
    assert result["status"] == "COMPLETED_SUCCESS"
    assert result["run_id"].startswith("CRESCA-RUN-")
    assert result["execution_duration_sec"] > 0

    # 2. Assertions on Sub-Tool Pipeline
    assert result["ingestion_metadata"]["schema_validation"] == "PASSED_STRICT"
    assert result["privacy_guardrail_report"]["total_records_scrubbed"] > 0
    assert result["statistical_summary"]["pca_analysis"]["pc1_explained_variance_pct"] > 40
    assert result["statistical_summary"]["poisson_forecasting"]["total_projected_cases"] > 0
    assert result["logistics_optimization"]["total_budget_utilized_idr"] > 0

    # 3. Assertions on Gemini 3.6 Strategic Reasoning Output
    assert result["strategic_synthesis"] is not None
    assert len(result["strategic_synthesis"]) > 200

    # 4. Assertions on PDF Document Generation
    assert "pdf_report_path" in result
    pdf_path = Path(result["pdf_report_path"])
    assert pdf_path.exists(), f"PDF report not found at {pdf_path}"
    assert pdf_path.stat().st_size > 1000, "Generated PDF file is empty or corrupted"

    # 5. Assertions on Firestore Persistence
    latest_runs = orchestrator.firestore_manager.get_latest_runs(limit=1)
    assert len(latest_runs) > 0
    assert latest_runs[0]["run_id"] == result["run_id"]

    print("\n=======================================================")
    print(f"Autonomous Run ID: {result['run_id']}")
    print(f"Duration: {result['execution_duration_sec']}s")
    print(f"PDF Generated: {pdf_path.name} ({pdf_path.stat().st_size / 1024:.1f} KB)")
    print(f"Firestore Verified: Run committed successfully")
    print(f"Total Projected Stunting: {result['statistical_summary']['poisson_forecasting']['total_projected_cases']} cases")
    print(f"Total Formula F-75 Allocated: {result['logistics_optimization']['total_f75_units']:,} tins")
    print("=======================================================")


if __name__ == "__main__":
    test_autonomous_agent_execution_loop()
