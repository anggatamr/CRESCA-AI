"""
Cresca AI — Statistical Engine Module
Implements:
1. Composite Demographic Vulnerability Index (CDVI) via Principal Component Analysis (PCA)
2. Risk Tier Segmentation via K-Means Clustering
3. 90-Day Stunting Incidence Projection via Poisson Generalized Linear Model (GLM)
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import statsmodels.api as sm
import statsmodels.formula.api as smf


class StatisticalEngine:
    """
    Production-grade mathematical and statistical processor for Cresca AI.
    Executes multivariate dimensionality reduction, spatial risk grouping, and incidence forecasting.
    """

    INDICATOR_COLUMNS = [
        "poor_sanitation_pct",
        "extreme_poverty_pct",
        "anemia_mothers_pct",
        "under_red_line_ratio",
        "posyandu_density_ratio",
        "dist_to_referral_clinic_km",
    ]

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=1, random_state=random_state)
        self.kmeans = KMeans(n_clusters=4, random_state=random_state, n_init=10)

    def compute_cdvi(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Computes the Composite Demographic Vulnerability Index (CDVI) using PCA (PC1).
        
        Formula:
        Z_i = (X_i - mu) / sigma
        CDVI_i = Sum(w_j * Z_ij), normalized to [0.0, 1.0] interval.
        """
        df_processed = df.copy()
        
        # Verify required columns exist
        missing_cols = [col for col in self.INDICATOR_COLUMNS if col not in df_processed.columns]
        if missing_cols:
            raise ValueError(f"Missing required indicator columns in dataset: {missing_cols}")

        # Standardize features
        features = df_processed[self.INDICATOR_COLUMNS].values
        scaled_features = self.scaler.fit_transform(features)

        # Fit PCA on the first principal component
        pc1 = self.pca.fit_transform(scaled_features).flatten()
        
        # Check alignment: ensure positive correlation with vulnerability
        # If mean correlation with indicators is negative, invert PC1
        correlations = [np.corrcoef(pc1, scaled_features[:, i])[0, 1] for i in range(len(self.INDICATOR_COLUMNS))]
        if np.mean(correlations) < 0:
            pc1 = -pc1

        # Min-max normalization to [0.0, 1.0] scale
        pc1_min, pc1_max = pc1.min(), pc1.max()
        if pc1_max > pc1_min:
            cdvi_normalized = (pc1 - pc1_min) / (pc1_max - pc1_min)
        else:
            cdvi_normalized = np.full_like(pc1, 0.5)

        df_processed["cdvi_score"] = np.round(cdvi_normalized, 4)

        # Feature contribution weights
        loadings = self.pca.components_[0]
        explained_variance_ratio = float(self.pca.explained_variance_ratio_[0])
        feature_weights = {
            col: round(float(abs(loadings[i])), 4)
            for i, col in enumerate(self.INDICATOR_COLUMNS)
        }

        pca_metadata = {
            "pc1_explained_variance_pct": round(explained_variance_ratio * 100, 2),
            "feature_weights": feature_weights,
            "mean_cdvi": round(float(df_processed["cdvi_score"].mean()), 4),
            "max_cdvi": round(float(df_processed["cdvi_score"].max()), 4),
            "min_cdvi": round(float(df_processed["cdvi_score"].min()), 4),
        }

        return df_processed, pca_metadata

    def segment_risk_clusters(self, df_with_cdvi: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Segments districts into 4 distinct risk tiers using K-Means Clustering on CDVI.
        Ranks clusters from CRITICAL (highest risk) to LOW (lowest risk).
        """
        df_clustered = df_with_cdvi.copy()
        
        if "cdvi_score" not in df_clustered.columns:
            raise ValueError("Dataframe must contain 'cdvi_score' before clustering.")

        # Fit K-Means on CDVI score
        cdvi_values = df_clustered[["cdvi_score"]].values
        df_clustered["cluster_raw"] = self.kmeans.fit_predict(cdvi_values)

        # Calculate mean CDVI per cluster to order tiers correctly
        cluster_means = df_clustered.groupby("cluster_raw")["cdvi_score"].mean().to_dict()
        sorted_clusters = sorted(cluster_means.items(), key=lambda x: x[1])

        # Map to standard risk tier names
        tier_names = ["LOW", "MODERATE", "HIGH", "CRITICAL"]
        cluster_to_tier = {cluster_id: tier_names[idx] for idx, (cluster_id, _) in enumerate(sorted_clusters)}

        df_clustered["risk_tier"] = df_clustered["cluster_raw"].map(cluster_to_tier)
        df_clustered.drop(columns=["cluster_raw"], inplace=True)

        tier_counts = df_clustered["risk_tier"].value_counts().to_dict()
        cluster_metadata = {
            "tier_distribution": {tier: tier_counts.get(tier, 0) for tier in tier_names},
            "tier_mean_cdvi": {
                tier_names[idx]: round(float(mean_val), 4)
                for idx, (_, mean_val) in enumerate(sorted_clusters)
            }
        }

        return df_clustered, cluster_metadata

    def forecast_poisson_incidence(self, df_clustered: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Fits a Poisson Generalized Linear Model (GLM) to project 90-day stunting incidence.
        
        Model specification:
        log(E[Y]) = beta_0 + beta_1 * cdvi_score + beta_2 * log(total_toddlers) + beta_3 * hist_trend
        """
        df_forecast = df_clustered.copy()

        # Compute historical growth factor from Q1 -> Q3
        df_forecast["hist_growth_trend"] = (
            (df_forecast["hist_stunting_q3"] - df_forecast["hist_stunting_q1"]) /
            (df_forecast["hist_stunting_q1"] + 1e-5)
        )
        df_forecast["log_toddlers"] = np.log(df_forecast["total_toddlers"])

        # Target variable: current active stunted toddlers
        y = df_forecast["current_active_stunted"].values
        X = df_forecast[["cdvi_score", "log_toddlers", "hist_growth_trend"]]
        X = sm.add_constant(X)

        # Fit Poisson GLM
        poisson_model = sm.GLM(y, X, family=sm.families.Poisson()).fit()

        # Predict expected stunting incidence for next 90 days
        predicted_means = poisson_model.predict(X)
        
        # Calculate 95% Confidence Intervals
        predictions = poisson_model.get_prediction(X)
        summary_frame = predictions.summary_frame(alpha=0.05)

        df_forecast["projected_stunting_90d"] = np.round(predicted_means).astype(int)
        df_forecast["proj_ci_lower_95"] = np.round(summary_frame["mean_ci_lower"]).astype(int)
        df_forecast["proj_ci_upper_95"] = np.round(summary_frame["mean_ci_upper"]).astype(int)
        df_forecast["urgency_rank"] = df_forecast["projected_stunting_90d"].rank(ascending=False, method="min").astype(int)

        # Clean temporary columns
        df_forecast.drop(columns=["log_toddlers", "hist_growth_trend"], inplace=True)

        glm_metadata = {
            "aic": round(float(poisson_model.aic), 2),
            "bic": round(float(poisson_model.bic_deviance), 2),
            "pseudo_r2": round(float(1 - (poisson_model.deviance / poisson_model.null_deviance)), 4),
            "total_projected_cases": int(df_forecast["projected_stunting_90d"].sum()),
            "critical_tier_projected_cases": int(
                df_forecast[df_forecast["risk_tier"] == "CRITICAL"]["projected_stunting_90d"].sum()
            ),
        }

        return df_forecast, glm_metadata

    def run_full_pipeline(self, df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Executes the complete end-to-end mathematical analysis pipeline:
        1. CDVI Extraction
        2. K-Means Risk Tiering
        3. Poisson 90-day Forecasting
        """
        df_cdvi, pca_meta = self.compute_cdvi(df_raw)
        df_tiered, cluster_meta = self.segment_risk_clusters(df_cdvi)
        df_final, glm_meta = self.forecast_poisson_incidence(df_tiered)

        # Sort results by urgency priority
        df_final.sort_values(by=["urgency_rank", "cdvi_score"], ascending=[True, False], inplace=True)

        pipeline_summary = {
            "pca_analysis": pca_meta,
            "clustering_analysis": cluster_meta,
            "poisson_forecasting": glm_meta,
            "districts_evaluated": len(df_final),
            "critical_districts": df_final[df_final["risk_tier"] == "CRITICAL"]["district_name"].tolist(),
        }

        return df_final, pipeline_summary
