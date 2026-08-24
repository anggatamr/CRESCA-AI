"""
Unit tests for StatisticalEngine in Cresca AI.
Validates mathematical integrity, PCA normalization, K-Means clustering, and Poisson GLM forecasting.
"""

from pathlib import Path
import pandas as pd
import pytest
from src.tools.statistical_engine import StatisticalEngine

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DISTRICTS_CSV = DATA_DIR / "synthetic_district_indicators.csv"

@pytest.fixture
def sample_district_data() -> pd.DataFrame:
    assert DISTRICTS_CSV.exists(), f"Synthetic dataset not found at {DISTRICTS_CSV}"
    df = pd.read_csv(DISTRICTS_CSV)
    return df

@pytest.fixture
def engine() -> StatisticalEngine:
    return StatisticalEngine(random_state=42)

def test_compute_cdvi(sample_district_data, engine):
    df_cdvi, meta = engine.compute_cdvi(sample_district_data)
    
    assert "cdvi_score" in df_cdvi.columns
    assert len(df_cdvi) == len(sample_district_data)
    
    # CDVI must be normalized between 0.0 and 1.0
    assert df_cdvi["cdvi_score"].min() >= 0.0
    assert df_cdvi["cdvi_score"].max() <= 1.0
    
    # Check PCA metadata
    assert meta["pc1_explained_variance_pct"] > 40.0
    assert len(meta["feature_weights"]) == len(StatisticalEngine.INDICATOR_COLUMNS)
    assert meta["max_cdvi"] >= meta["min_cdvi"]

def test_segment_risk_clusters(sample_district_data, engine):
    df_cdvi, _ = engine.compute_cdvi(sample_district_data)
    df_clustered, meta = engine.segment_risk_clusters(df_cdvi)
    
    assert "risk_tier" in df_clustered.columns
    expected_tiers = {"LOW", "MODERATE", "HIGH", "CRITICAL"}
    actual_tiers = set(df_clustered["risk_tier"].unique())
    assert actual_tiers.issubset(expected_tiers)
    
    # Verify hierarchical order: CRITICAL mean CDVI > HIGH > MODERATE > LOW
    means = meta["tier_mean_cdvi"]
    assert means["CRITICAL"] >= means["HIGH"]
    assert means["HIGH"] >= means["MODERATE"]
    assert means["MODERATE"] >= means["LOW"]

def test_forecast_poisson_incidence(sample_district_data, engine):
    df_cdvi, _ = engine.compute_cdvi(sample_district_data)
    df_clustered, _ = engine.segment_risk_clusters(df_cdvi)
    df_forecast, meta = engine.forecast_poisson_incidence(df_clustered)
    
    assert "projected_stunting_90d" in df_forecast.columns
    assert "proj_ci_lower_95" in df_forecast.columns
    assert "proj_ci_upper_95" in df_forecast.columns
    assert "urgency_rank" in df_forecast.columns
    
    # Verify non-negativity and confidence interval bounds
    assert (df_forecast["projected_stunting_90d"] >= 0).all()
    assert (df_forecast["proj_ci_upper_95"] >= df_forecast["proj_ci_lower_95"]).all()
    assert meta["total_projected_cases"] > 0
    assert meta["critical_tier_projected_cases"] > 0

def test_run_full_pipeline(sample_district_data, engine):
    df_final, summary = engine.run_full_pipeline(sample_district_data)
    
    assert len(df_final) == len(sample_district_data)
    assert "cdvi_score" in df_final.columns
    assert "risk_tier" in df_final.columns
    assert "projected_stunting_90d" in df_final.columns
    assert summary["districts_evaluated"] == len(sample_district_data)
    assert len(summary["critical_districts"]) > 0
    
    print("\n--- Pipeline Summary ---")
    print(f"Districts Evaluated: {summary['districts_evaluated']}")
    print(f"Critical Districts: {summary['critical_districts']}")
    print(f"Total 90-Day Projected Stunting Cases: {summary['poisson_forecasting']['total_projected_cases']}")
    print("------------------------")
