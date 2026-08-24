"""
End-to-End Integration Test for CrescaAgentOrchestrator.
Validates that the autonomous agent loop executes seamlessly without human intervention.
"""

import pytest
from src.agent.orchestrator import CrescaAgentOrchestrator


def test_autonomous_agent_execution_loop():
    orchestrator = CrescaAgentOrchestrator()
    result = orchestrator.execute_autonomous_run(trigger_source="INTEGRATION_TEST_RUNNER")

    # Assertions on Execution Lifecycle
    assert result["status"] == "COMPLETED_SUCCESS"
    assert result["run_id"].startswith("CRESCA-RUN-")
    assert result["execution_duration_sec"] > 0

    # Assertions on Sub-Tool Pipeline
    assert result["ingestion_metadata"]["schema_validation"] == "PASSED_STRICT"
    assert result["privacy_guardrail_report"]["total_records_scrubbed"] > 0
    assert result["statistical_summary"]["pca_analysis"]["pc1_explained_variance_pct"] > 40
    assert result["statistical_summary"]["poisson_forecasting"]["total_projected_cases"] > 0
    assert result["logistics_optimization"]["total_budget_utilized_idr"] > 0

    # Assertions on Gemini 3.6 Strategic Reasoning Output
    assert result["strategic_synthesis"] is not None
    assert len(result["strategic_synthesis"]) > 200
    assert len(result["execution_logs"]) >= 5

    print("\n=======================================================")
    print(f"Autonomous Run ID: {result['run_id']}")
    print(f"Duration: {result['execution_duration_sec']}s")
    print(f"Total Projected Stunting: {result['statistical_summary']['poisson_forecasting']['total_projected_cases']} cases")
    print(f"Total Formula F-75 Allocated: {result['logistics_optimization']['total_f75_units']:,} tins")
    print("\n--- Gemini Strategic Reasoning Preview ---")
    print(result["strategic_synthesis"][:500] + "...\n[Full Synthesis Available]")
    print("=======================================================")


if __name__ == "__main__":
    test_autonomous_agent_execution_loop()
