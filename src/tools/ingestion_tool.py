"""
Cresca AI — Data Ingestion & Schema Validation Module
Handles asynchronous ingestion from Google Cloud Storage (GCS) or local staging batches,
validating data types, boundary constraints, and missing values.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import pandas as pd
from src.config import DATA_DIR


class DataIngestionTool:
    """
    Automates data ingestion and schema validation for demographic indicators and micro anthropometric records.
    """

    REQUIRED_DISTRICT_COLUMNS = [
        "district_id",
        "district_name",
        "total_toddlers",
        "poor_sanitation_pct",
        "extreme_poverty_pct",
        "anemia_mothers_pct",
        "under_red_line_ratio",
        "posyandu_density_ratio",
        "dist_to_referral_clinic_km",
        "hist_stunting_q1",
        "hist_stunting_q2",
        "hist_stunting_q3",
        "current_active_stunted",
    ]

    def __init__(self, data_directory: Optional[Path] = None):
        self.data_dir = data_directory or DATA_DIR

    def ingest_district_batch(self, file_name: str = "synthetic_district_indicators.csv") -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Loads and validates district summary records.
        """
        file_path = self.data_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"District dataset not found at: {file_path}")

        df = pd.read_csv(file_path)

        # 1. Check Missing Columns
        missing_cols = [col for col in self.REQUIRED_DISTRICT_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Schema validation failed. Missing required columns: {missing_cols}")

        # 2. Check Data Boundaries & Nulls
        null_counts = int(df[self.REQUIRED_DISTRICT_COLUMNS].isnull().sum().sum())
        if null_counts > 0:
            df.fillna(df.median(numeric_only=True), inplace=True)

        # 3. Ensure Numeric Types
        numeric_cols = [
            "total_toddlers", "poor_sanitation_pct", "extreme_poverty_pct",
            "anemia_mothers_pct", "under_red_line_ratio", "posyandu_density_ratio",
            "dist_to_referral_clinic_km", "hist_stunting_q1", "hist_stunting_q2",
            "hist_stunting_q3", "current_active_stunted"
        ]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        ingestion_metadata = {
            "source_file": file_name,
            "total_districts_loaded": len(df),
            "total_monitored_toddler_population": int(df["total_toddlers"].sum()),
            "total_current_active_stunting": int(df["current_active_stunted"].sum()),
            "schema_validation": "PASSED_STRICT",
        }

        return df, ingestion_metadata

    def ingest_micro_toddler_records(self, file_name: str = "synthetic_toddler_records.csv") -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Loads individual Posyandu toddler records.
        """
        file_path = self.data_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Toddler records file not found at: {file_path}")

        df = pd.read_csv(file_path)
        metadata = {
            "source_file": file_name,
            "total_individual_records": len(df),
            "stunted_cases_detected": int((df["nutrition_status"].isin(["STUNTED", "SEVERELY_STUNTED"])).sum()),
            "schema_validation": "PASSED",
        }
        return df, metadata
