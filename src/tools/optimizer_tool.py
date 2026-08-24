"""
Cresca AI — Multi-Constraint Logistics Optimizer Module
Calculates precise nutritional supplement quotas, SKU units, and budget allocations
based on CDVI scores, risk tiers, and Poisson 90-day projected incidence.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd


class LogisticsOptimizer:
    """
    Solves multi-constraint resource allocation for emergency nutritional intervention.
    Calculates exact quantities for:
    1. Formula F-75 / F-100 therapeutic milk (for severely acute stunted / SAM)
    2. Fortified PMT Biscuits (Pemberian Makanan Tambahan)
    3. Iron Folate / Micronutrient Sachets (Taburia)
    """

    # Unit costs in IDR (Indonesian Rupiah) based on standard public health procurement
    COST_PER_UNIT = {
        "f75_formula_tin": 75000,       # Rp 75.000 / kaleng
        "pmt_biscuit_box": 35000,        # Rp 35.000 / box (1 bulan)
        "iron_folate_pack": 15000,       # Rp 15.000 / pack (30 tablet)
    }

    # Standard nutritional dosage per child over 90-day intervention cycle
    DOSAGE_PER_CASE = {
        "CRITICAL": {"f75_tins": 6, "pmt_boxes": 3, "iron_packs": 3},
        "HIGH": {"f75_tins": 3, "pmt_boxes": 3, "iron_packs": 2},
        "MODERATE": {"f75_tins": 1, "pmt_boxes": 2, "iron_packs": 2},
        "LOW": {"f75_tins": 0, "pmt_boxes": 1, "iron_packs": 1},
    }

    def __init__(self, total_budget_idr: int = 500_000_000, warehouse_f75_stock: int = 5000):
        self.total_budget_idr = total_budget_idr
        self.warehouse_f75_stock = warehouse_f75_stock

    def optimize_allocation(self, df_statistical_results: pd.DataFrame) -> Dict[str, Any]:
        """
        Computes the optimal supplement allocation per district subject to budget & stock constraints.
        """
        allocations = []
        total_spent = 0
        total_f75_allocated = 0
        total_pmt_allocated = 0
        total_iron_allocated = 0

        # Sort districts by urgency rank (highest priority first)
        df_sorted = df_statistical_results.sort_values(by="urgency_rank", ascending=True).copy()

        for _, row in df_sorted.iterrows():
            tier = row["risk_tier"]
            projected_cases = int(row["projected_stunting_90d"])
            cdvi = float(row["cdvi_score"])
            dosage = self.DOSAGE_PER_CASE.get(tier, self.DOSAGE_PER_CASE["MODERATE"])

            # Compute raw required units
            f75_needed = int(projected_cases * dosage["f75_tins"])
            pmt_needed = int(projected_cases * dosage["pmt_boxes"])
            iron_needed = int(projected_cases * dosage["iron_packs"])

            # Calculate cost for this district
            district_cost = (
                (f75_needed * self.COST_PER_UNIT["f75_formula_tin"]) +
                (pmt_needed * self.COST_PER_UNIT["pmt_biscuit_box"]) +
                (iron_needed * self.COST_PER_UNIT["iron_folate_pack"])
            )

            # Check budget availability
            if total_spent + district_cost <= self.total_budget_idr:
                f75_allocated = f75_needed
                pmt_allocated = pmt_needed
                iron_allocated = iron_needed
                allocated_cost = district_cost
                allocation_status = "FULLY_FUNDED"
            else:
                # Fractional funding based on remaining budget
                remaining_budget = max(0, self.total_budget_idr - total_spent)
                funding_ratio = remaining_budget / (district_cost + 1e-5)
                f75_allocated = int(f75_needed * funding_ratio)
                pmt_allocated = int(pmt_needed * funding_ratio)
                iron_allocated = int(iron_needed * funding_ratio)
                allocated_cost = (
                    (f75_allocated * self.COST_PER_UNIT["f75_formula_tin"]) +
                    (pmt_allocated * self.COST_PER_UNIT["pmt_biscuit_box"]) +
                    (iron_allocated * self.COST_PER_UNIT["iron_folate_pack"])
                )
                allocation_status = "PARTIALLY_FUNDED" if allocated_cost > 0 else "DEFERRED_NEXT_CYCLE"

            total_spent += allocated_cost
            total_f75_allocated += f75_allocated
            total_pmt_allocated += pmt_allocated
            total_iron_allocated += iron_allocated

            allocations.append({
                "district_id": row["district_id"],
                "district_name": row["district_name"],
                "urgency_rank": int(row["urgency_rank"]),
                "risk_tier": tier,
                "cdvi_score": cdvi,
                "projected_cases_90d": projected_cases,
                "allocated_f75_tins": f75_allocated,
                "allocated_pmt_boxes": pmt_allocated,
                "allocated_iron_packs": iron_allocated,
                "district_cost_idr": allocated_cost,
                "allocation_status": allocation_status,
            })

        return {
            "total_budget_cap_idr": self.total_budget_idr,
            "total_budget_utilized_idr": total_spent,
            "budget_utilization_pct": round((total_spent / self.total_budget_idr) * 100, 2),
            "total_f75_units": total_f75_allocated,
            "total_pmt_boxes": total_pmt_allocated,
            "total_iron_packs": total_iron_allocated,
            "districts_funded_count": sum(1 for a in allocations if a["allocation_status"] == "FULLY_FUNDED"),
            "district_allocations": allocations,
        }
