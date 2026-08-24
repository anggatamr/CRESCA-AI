"""
Cresca AI — Autonomous Agent Orchestrator Module
Coordinates the end-to-end background agent loop:
Ingestion -> Privacy Scrubbing -> Statistical Modeling -> Multi-Constraint Optimization -> Gemini 3.6 Strategic Reasoning.
"""

import time
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from google import genai
from google.genai import types

from src.config import (
    GEMINI_API_KEY,
    REASONING_MODEL,
    FALLBACK_REASONING_MODEL,
    GCP_PROJECT_ID,
)
from src.tools.ingestion_tool import DataIngestionTool
from src.tools.privacy_guard import PrivacyGuard
from src.tools.statistical_engine import StatisticalEngine
from src.tools.optimizer_tool import LogisticsOptimizer
from src.agent.prompts import SYSTEM_INSTRUCTION, STRATEGIC_REASONING_PROMPT


class CrescaAgentOrchestrator:
    """
    Autonomous Taskmaster Agent Orchestrator for Cresca AI Sentinel.
    Runs asynchronously in the background to analyze demographic health data and dispatch action plans.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required to initialize CrescaAgentOrchestrator.")

        # Initialize Google GenAI client
        self.client = genai.Client(api_key=self.api_key)

        # Initialize agent sub-tools
        self.ingestion_tool = DataIngestionTool()
        self.privacy_guard = PrivacyGuard()
        self.stat_engine = StatisticalEngine(random_state=42)
        self.optimizer = LogisticsOptimizer(total_budget_idr=500_000_000)

    def execute_autonomous_run(self, trigger_source: str = "CLOUD_SCHEDULER_CRON") -> Dict[str, Any]:
        """
        Executes a complete autonomous cycle without requiring user intervention.
        """
        start_time = time.time()
        run_id = f"CRESCA-RUN-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        logs = []

        def log_step(message: str):
            timestamp = datetime.now(timezone.utc).isoformat()
            logs.append(f"[{timestamp}] {message}")
            print(f"[Cresca Agent] {message}")

        log_step(f"Initializing Autonomous Execution Loop: {run_id} (Trigger: {trigger_source})")

        # Step 1: Data Ingestion & Schema Validation
        log_step("Step 1/5: Ingesting demographic indicator batch...")
        df_districts, ingestion_meta = self.ingestion_tool.ingest_district_batch()
        df_micro, micro_meta = self.ingestion_tool.ingest_micro_toddler_records()
        log_step(f"Ingested {len(df_districts)} districts and {len(df_micro)} micro records successfully.")

        # Step 2: Privacy-Preserving PII Redaction (Gemma 2 Guardrail)
        log_step("Step 2/5: Executing Gemma 2 zero-shot PII sanitization...")
        df_micro_clean, privacy_report = self.privacy_guard.sanitize_micro_records(df_micro)
        log_step(f"Sanitized {privacy_report['total_records_scrubbed']} records. PII masked: {privacy_report['pii_fields_redacted']}.")

        # Step 3: Statistical Modeling (PCA CDVI, K-Means, Poisson GLM)
        log_step("Step 3/5: Running Statistical Engine (PCA CDVI + K-Means + Poisson GLM)...")
        df_analyzed, stat_summary = self.stat_engine.run_full_pipeline(df_districts)
        log_step(f"Statistical pipeline complete. PC1 Explained Variance: {stat_summary['pca_analysis']['pc1_explained_variance_pct']}%.")
        log_step(f"Projected 90-Day Stunting Cases: {stat_summary['poisson_forecasting']['total_projected_cases']} across 21 districts.")

        # Step 4: Multi-Constraint Logistics Optimization
        log_step("Step 4/5: Solving multi-constraint logistics optimization...")
        logistics_results = self.optimizer.optimize_allocation(df_analyzed)
        log_step(f"Logistics optimization solved. Budget utilized: IDR {logistics_results['total_budget_utilized_idr']:,} ({logistics_results['budget_utilization_pct']}%).")
        log_step(f"Allocated: {logistics_results['total_f75_units']:,} F-75 tins, {logistics_results['total_pmt_boxes']:,} PMT boxes, {logistics_results['total_iron_packs']:,} Iron packs.")

        # Step 5: Strategic Decision Synthesis via Gemini 3.6 Flash
        log_step(f"Step 5/5: Engaging Strategic Reasoning Model ({REASONING_MODEL})...")
        
        # Prepare context for prompt
        top_5_allocations = json.dumps(logistics_results["district_allocations"][:5], indent=2)
        prompt_content = STRATEGIC_REASONING_PROMPT.format(
            districts_evaluated=stat_summary["districts_evaluated"],
            total_toddlers=ingestion_meta["total_monitored_toddler_population"],
            current_active_stunting=ingestion_meta["total_current_active_stunting"],
            total_projected_cases=stat_summary["poisson_forecasting"]["total_projected_cases"],
            pc1_explained_variance_pct=stat_summary["pca_analysis"]["pc1_explained_variance_pct"],
            feature_weights=json.dumps(stat_summary["pca_analysis"]["feature_weights"]),
            critical_districts=", ".join(stat_summary["critical_districts"]),
            tier_distribution=json.dumps(stat_summary["clustering_analysis"]["tier_distribution"]),
            total_budget_cap=f"{logistics_results['total_budget_cap_idr']:,}",
            total_budget_utilized=f"{logistics_results['total_budget_utilized_idr']:,}",
            budget_utilization_pct=logistics_results["budget_utilization_pct"],
            total_f75_units=f"{logistics_results['total_f75_units']:,}",
            total_pmt_boxes=f"{logistics_results['total_pmt_boxes']:,}",
            total_iron_packs=f"{logistics_results['total_iron_packs']:,}",
            top_district_allocations=top_5_allocations,
        )

        try:
            response = self.client.models.generate_content(
                model=REASONING_MODEL,
                contents=prompt_content,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.2,
                )
            )
            strategic_synthesis = response.text
            log_step("Gemini strategic reasoning synthesis generated successfully.")
        except Exception as e:
            log_step(f"Primary model {REASONING_MODEL} failed ({str(e)}), attempting fallback to {FALLBACK_REASONING_MODEL}...")
            response = self.client.models.generate_content(
                model=FALLBACK_REASONING_MODEL,
                contents=prompt_content,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.2,
                )
            )
            strategic_synthesis = response.text
            log_step("Fallback model reasoning synthesis completed.")

        duration_sec = round(time.time() - start_time, 2)
        log_step(f"Autonomous run {run_id} completed successfully in {duration_sec}s.")

        # Compile full execution payload
        execution_payload = {
            "run_id": run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trigger_source": trigger_source,
            "status": "COMPLETED_SUCCESS",
            "execution_duration_sec": duration_sec,
            "ingestion_metadata": ingestion_meta,
            "privacy_guardrail_report": privacy_report,
            "statistical_summary": stat_summary,
            "logistics_optimization": logistics_results,
            "strategic_synthesis": strategic_synthesis,
            "analyzed_districts_data": df_analyzed.to_dict(orient="records"),
            "execution_logs": logs,
        }

        return execution_payload
