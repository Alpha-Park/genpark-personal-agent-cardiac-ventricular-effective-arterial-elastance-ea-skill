"""
Example usage of Cardiac Ventriculo-Arterial Coupling (Ea/Ees) Skill.
Demonstrates optimal physiological coupling vs arterial stiffening uncoupling.
"""

import json
from client import VentriculoArterialCouplingClient


def main():
    print("=== Testing Cardiac Ventriculo-Arterial Coupling (Ea/Ees) Skill ===")
    client = VentriculoArterialCouplingClient()

    # 1. Healthy young adult with optimal coupling (BP=115/75, SV=75 mL, LVEF=0.62)
    res_optimal = client.evaluate_coupling(
        systolic_bp_mmhg=115.0,
        diastolic_bp_mmhg=75.0,
        stroke_volume_ml=75.0,
        left_ventricular_ejection_fraction=0.62
    )
    print("\n[Case 1: Optimal Ventriculo-Arterial Coupling]")
    print(json.dumps(res_optimal, indent=2))

    # 2. Hypertensive arterial stiffening / elevated afterload (BP=160/95, SV=60 mL, LVEF=0.48)
    res_stiffened = client.evaluate_coupling(
        systolic_bp_mmhg=160.0,
        diastolic_bp_mmhg=95.0,
        stroke_volume_ml=60.0,
        left_ventricular_ejection_fraction=0.48
    )
    print("\n[Case 2: Elevated Arterial Elastance / Uncoupling]")
    print(json.dumps(res_stiffened, indent=2))

    # Assertions
    assert 0.6 <= res_optimal["ventriculo_arterial_coupling_ratio"] <= 1.2
    assert res_stiffened["effective_arterial_elastance_ea"] > res_optimal["effective_arterial_elastance_ea"]
    assert res_stiffened["mechanical_efficiency_percentage"] < res_optimal["mechanical_efficiency_percentage"]
    print("\n[SUCCESS] Ventriculo-Arterial Coupling tests passed!")


if __name__ == "__main__":
    main()
