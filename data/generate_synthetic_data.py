"""
Synthetic Demographic & Anthropometric Data Generator
Produces realistic, privacy-preserving micro-demographic records across 21 districts/Posyandu.
Ensures zero exposure of real-world sensitive PII.
"""

import json
import random
from pathlib import Path
import numpy as np
import pandas as pd

# Set deterministic random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

OUTPUT_DIR = Path(__file__).resolve().parent

# 21 Real-inspired administrative districts (e.g., North Sumatra / Medan regional area)
DISTRICTS = [
    {"id": "DIST-01", "name": "Medan Belawan", "lat": 3.7781, "lon": 98.6833, "base_risk": 0.85},
    {"id": "DIST-02", "name": "Medan Labuhan", "lat": 3.7125, "lon": 98.6750, "base_risk": 0.78},
    {"id": "DIST-03", "name": "Medan Marelan", "lat": 3.6890, "lon": 98.6500, "base_risk": 0.65},
    {"id": "DIST-04", "name": "Medan Deli", "lat": 3.6540, "lon": 98.6700, "base_risk": 0.72},
    {"id": "DIST-05", "name": "Medan Tembung", "lat": 3.5980, "lon": 98.7150, "base_risk": 0.58},
    {"id": "DIST-06", "name": "Medan Denai", "lat": 3.5650, "lon": 98.7100, "base_risk": 0.62},
    {"id": "DIST-07", "name": "Medan Amplas", "lat": 3.5350, "lon": 98.7050, "base_risk": 0.55},
    {"id": "DIST-08", "name": "Medan Johor", "lat": 3.5250, "lon": 98.6650, "base_risk": 0.35},
    {"id": "DIST-09", "name": "Medan Tuntungan", "lat": 3.5100, "lon": 98.6050, "base_risk": 0.40},
    {"id": "DIST-10", "name": "Medan Selayang", "lat": 3.5450, "lon": 98.6250, "base_risk": 0.30},
    {"id": "DIST-11", "name": "Medan Sunggal", "lat": 3.5850, "lon": 98.6150, "base_risk": 0.38},
    {"id": "DIST-12", "name": "Medan Helvetia", "lat": 3.6150, "lon": 98.6400, "base_risk": 0.45},
    {"id": "DIST-13", "name": "Medan Barat", "lat": 3.6050, "lon": 98.6650, "base_risk": 0.42},
    {"id": "DIST-14", "name": "Medan Timur", "lat": 3.6100, "lon": 98.6900, "base_risk": 0.48},
    {"id": "DIST-15", "name": "Medan Perjuangan", "lat": 3.5950, "lon": 98.6950, "base_risk": 0.52},
    {"id": "DIST-16", "name": "Medan Kota", "lat": 3.5750, "lon": 98.6850, "base_risk": 0.33},
    {"id": "DIST-17", "name": "Medan Maimun", "lat": 3.5700, "lon": 98.6750, "base_risk": 0.50},
    {"id": "DIST-18", "name": "Medan Polonia", "lat": 3.5550, "lon": 98.6650, "base_risk": 0.28},
    {"id": "DIST-19", "name": "Medan Baru", "lat": 3.5700, "lon": 98.6550, "base_risk": 0.25},
    {"id": "DIST-20", "name": "Medan Petisah", "lat": 3.5900, "lon": 98.6600, "base_risk": 0.29},
    {"id": "DIST-21", "name": "Medan Area", "lat": 3.5750, "lon": 98.7000, "base_risk": 0.49},
]

FIRST_NAMES = ["Budi", "Aisyah", "Rizky", "Siti", "Fajar", "Putri", "Dimas", "Nurul", "Kevin", "Dewi", "Bayu", "Lestari", "Rian", "Anisa", "Rafi", "Tiara", "Galang", "Zahra", "Aditya", "Melati"]
LAST_NAMES = ["Pratama", "Siregar", "Nasution", "Lubis", "Harahap", "Sitorus", "Sinaga", "Ginting", "Tarigan", "Tambunan", "Pangaribuan", "Hutapea", "Simanjuntak", "Sembiring", "Pasaribu"]

def generate_district_summary_data() -> pd.DataFrame:
    """Generates macro/district level indicators for PCA & Poisson analysis."""
    rows = []
    for d in DISTRICTS:
        base = d["base_risk"]
        total_toddlers = int(np.random.normal(loc=1200, scale=250))
        total_toddlers = max(total_toddlers, 500)
        
        # Correlated indicators based on baseline risk
        poor_sanitation_pct = np.clip(np.random.normal(loc=base * 70, scale=8), 5, 95)
        extreme_poverty_pct = np.clip(np.random.normal(loc=base * 45, scale=6), 2, 80)
        anemia_mothers_pct = np.clip(np.random.normal(loc=base * 50, scale=7), 5, 85)
        under_red_line_ratio = np.clip(np.random.normal(loc=base * 0.25, scale=0.03), 0.02, 0.45)
        posyandu_density_ratio = np.clip(np.random.normal(loc=150 + base * 100, scale=25), 80, 350)
        dist_to_referral_clinic_km = np.clip(np.random.normal(loc=2.0 + base * 6.0, scale=1.5), 0.5, 15.0)
        
        # Historical baseline stunting incidence (last 3 quarters)
        hist_q1 = int(total_toddlers * (base * 0.18 + np.random.uniform(-0.02, 0.02)))
        hist_q2 = int(total_toddlers * (base * 0.19 + np.random.uniform(-0.02, 0.02)))
        hist_q3 = int(total_toddlers * (base * 0.20 + np.random.uniform(-0.02, 0.02)))
        current_active_stunted = hist_q3
        
        rows.append({
            "district_id": d["id"],
            "district_name": d["name"],
            "latitude": d["lat"],
            "longitude": d["lon"],
            "total_toddlers": total_toddlers,
            "poor_sanitation_pct": round(poor_sanitation_pct, 2),
            "extreme_poverty_pct": round(extreme_poverty_pct, 2),
            "anemia_mothers_pct": round(anemia_mothers_pct, 2),
            "under_red_line_ratio": round(under_red_line_ratio, 4),
            "posyandu_density_ratio": round(posyandu_density_ratio, 2),
            "dist_to_referral_clinic_km": round(dist_to_referral_clinic_km, 2),
            "hist_stunting_q1": max(hist_q1, 5),
            "hist_stunting_q2": max(hist_q2, 5),
            "hist_stunting_q3": max(hist_q3, 5),
            "current_active_stunted": max(current_active_stunted, 5),
        })
        
    df = pd.DataFrame(rows)
    return df

def generate_micro_toddler_records(n_records: int = 1000) -> pd.DataFrame:
    """Generates synthetic toddler anthropometric records with synthetic PII for testing Gemma 2 redaction."""
    records = []
    for i in range(1, n_records + 1):
        district = random.choice(DISTRICTS)
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        child_name = f"{first_name} {last_name}"
        parent_name = f"{random.choice(FIRST_NAMES)} {last_name}"
        nik = f"1271{random.randint(10, 99)}{random.randint(100000, 999999)}{random.randint(1000, 9999)}"
        
        age_months = random.randint(6, 59)
        gender = random.choice(["M", "F"])
        
        # Generate height and weight based on age and district base risk
        base_h = 65 + (age_months * 0.7)
        base_w = 7.0 + (age_months * 0.25)
        
        risk_factor = district["base_risk"]
        height_cm = np.clip(np.random.normal(loc=base_h - (risk_factor * 4.5), scale=3.5), 50.0, 120.0)
        weight_kg = np.clip(np.random.normal(loc=base_w - (risk_factor * 1.8), scale=1.2), 4.5, 25.0)
        
        # Anthropometric standard Z-scores approximation (WHO child growth standards)
        z_haz = (height_cm - base_h) / 3.0  # Height-for-Age Z-Score
        z_waz = (weight_kg - base_w) / 1.1  # Weight-for-Age Z-Score
        
        nutrition_status = "NORMAL"
        if z_haz < -3.0:
            nutrition_status = "SEVERELY_STUNTED"
        elif z_haz < -2.0:
            nutrition_status = "STUNTED"
        elif z_haz < -1.0:
            nutrition_status = "POTENTIAL_RISK"
            
        records.append({
            "child_id": f"CHD-2026-{i:05d}",
            "synthetic_nik": nik,
            "synthetic_name": child_name,
            "synthetic_parent_name": parent_name,
            "district_id": district["id"],
            "district_name": district["name"],
            "posyandu_name": f"Posyandu Melati {random.randint(1, 8)}",
            "age_months": age_months,
            "gender": gender,
            "height_cm": round(height_cm, 1),
            "weight_kg": round(weight_kg, 2),
            "z_haz_score": round(z_haz, 2),
            "z_waz_score": round(z_waz, 2),
            "nutrition_status": nutrition_status,
            "has_exclusive_breastfeeding": random.choice([True, False]) if age_months <= 24 else False,
            "water_source_access": random.choices(["PDAM", "Sumur Terlindung", "Air Sungai / Tak Terlindung"], weights=[0.4, 0.4, 0.2])[0],
        })
        
    df = pd.DataFrame(records)
    return df

def main():
    print("Generating Cresca AI synthetic demographic dataset...")
    
    # 1. District Macro Indicators
    df_districts = generate_district_summary_data()
    districts_csv_path = OUTPUT_DIR / "synthetic_district_indicators.csv"
    df_districts.to_csv(districts_csv_path, index=False)
    print(f"Saved: {districts_csv_path} ({len(df_districts)} districts)")
    
    # 2. Micro Toddler Anthropometric Records
    df_toddlers = generate_micro_toddler_records(n_records=1200)
    toddlers_csv_path = OUTPUT_DIR / "synthetic_toddler_records.csv"
    df_toddlers.to_csv(toddlers_csv_path, index=False)
    print(f"Saved: {toddlers_csv_path} ({len(df_toddlers)} micro records)")
    
    # Summary JSON Metadata
    metadata = {
        "dataset_name": "Cresca AI Synthetic Demographic & Anthropometric Benchmark",
        "generated_at": "2026-08-24",
        "district_count": len(df_districts),
        "total_micro_records": len(df_toddlers),
        "stunted_micro_records_count": int((df_toddlers["nutrition_status"].isin(["STUNTED", "SEVERELY_STUNTED"])).sum()),
        "compliance_note": "100% synthetic mathematical generation for privacy compliance."
    }
    metadata_path = OUTPUT_DIR / "dataset_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata: {metadata_path}")
    print("Synthetic data generation completed successfully!")

if __name__ == "__main__":
    main()
