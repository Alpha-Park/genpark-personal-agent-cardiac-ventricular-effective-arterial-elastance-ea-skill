"""
Cardiac Ventriculo-Arterial Coupling & Effective Arterial Elastance (Ea) Client.
Zero-mock pure Python standard library implementation.
Calculates Effective Arterial Elastance (Ea), Left Ventricular End-Systolic Elastance (Ees),
Ventriculo-Arterial Coupling Ratio (Ea / Ees), and mechanical stroke work efficiency.
"""

import math
from typing import Dict, Any, Optional


class VentriculoArterialCouplingClient:
    """
    Computes Effective Arterial Elastance (Ea = ESP / SV) and non-invasive single-beat
    end-systolic elastance (Ees) to evaluate cardiovascular energetic coupling efficiency.
    """

    def __init__(self):
        pass

    def evaluate_coupling(
        self,
        systolic_bp_mmhg: float,
        diastolic_bp_mmhg: float,
        stroke_volume_ml: float,
        pre_ejection_period_ms: float = 80.0,
        total_ejection_time_ms: float = 300.0,
        left_ventricular_ejection_fraction: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates Ea, Ees, Ea/Ees ratio, and mechanical efficiency.
        systolic_bp_mmhg: SBP (mmHg).
        diastolic_bp_mmhg: DBP (mmHg).
        stroke_volume_ml: Left ventricular stroke volume (mL).
        pre_ejection_period_ms: PEP in ms (systolic time interval).
        total_ejection_time_ms: LVET in ms.
        left_ventricular_ejection_fraction: LVEF fraction (e.g. 0.60 for 60%, optional).
        """
        if systolic_bp_mmhg <= diastolic_bp_mmhg or diastolic_bp_mmhg <= 0:
            raise ValueError("Systolic BP must exceed Diastolic BP, and both positive.")
        if stroke_volume_ml <= 0:
            raise ValueError("Stroke volume must be strictly positive.")
        if pre_ejection_period_ms <= 0 or total_ejection_time_ms <= 0:
            raise ValueError("Systolic time intervals must be positive.")

        # End-systolic pressure estimation: ESP is widely validated as 0.9 * SBP
        end_systolic_pressure_mmhg = 0.90 * systolic_bp_mmhg

        # Effective Arterial Elastance: Ea = ESP / SV (mmHg/mL)
        # Represents total vascular afterload (resistance, compliance, impedance, heart rate)
        ea_mmhg_ml = end_systolic_pressure_mmhg / stroke_volume_ml

        # End-Systolic Elastance (Ees): LV contractility / chamber stiffness
        # If LVEF is provided, Chen's single-beat approximation or standard ratio:
        # Ees = ESP / (ESV - V0). Since SV = EDV - ESV and EF = SV / EDV:
        # ESV = SV * (1 - EF) / EF. Assuming negligible V0: Ees ~ ESP / ESV = Ea * EF / (1 - EF)
        if left_ventricular_ejection_fraction is not None and 0.10 <= left_ventricular_ejection_fraction < 1.0:
            lvef = left_ventricular_ejection_fraction
            esv_ml = stroke_volume_ml * (1.0 - lvef) / lvef
            ees_mmhg_ml = end_systolic_pressure_mmhg / esv_ml
        else:
            # Systolic time interval surrogate (PEP / LVET):
            # Ratio of pre-ejection to ejection time correlates inversely with Ees
            # Normalized approximation: Ees ~ Ea / (0.8 * (LVET / PEP) - 0.5)
            time_ratio = total_ejection_time_ms / pre_ejection_period_ms
            ees_mmhg_ml = ea_mmhg_ml / max(0.4, (0.45 * time_ratio))
            lvef = None
            esv_ml = None

        # Ventriculo-Arterial Coupling Ratio: VAC = Ea / Ees
        vac_ratio = ea_mmhg_ml / ees_mmhg_ml

        # Stroke Work Efficiency (SW / (SW + PVA)):
        # Optimal mechanical work transfer occurs at Ea / Ees = 1.0.
        # Optimal metabolic oxygen consumption efficiency occurs at Ea / Ees = 0.5 - 0.7.
        mechanical_efficiency_pct = (1.0 / (1.0 + (0.5 * vac_ratio))) * 100.0

        if vac_ratio < 0.6:
            classification = "Hyper-Contractile / Low Afterload State"
            coupling_status = "Supranormal left ventricular inotropy relative to low arterial impedance."
            optimization_window = "High mechanical efficiency, sub-maximal stroke work transfer."
        elif vac_ratio <= 1.2:
            classification = "Optimal Ventriculo-Arterial Coupling (Ea/Ees: 0.6 - 1.2)"
            coupling_status = "Perfect hemodynamic impedance match between LV myocardial pump and systemic arterial tree."
            optimization_window = "Gold standard zone for cardiac mechanical efficiency and minimal oxygen cost."
        elif vac_ratio <= 1.6:
            classification = "Mild Ventriculo-Arterial Uncoupling / Elevated Afterload"
            coupling_status = "Arterial stiffening or vasoconstriction outpaces ventricular contractile reserve."
            optimization_window = "Early uncoupling; left ventricle performs excess work to overcome systemic impedance."
        else:
            classification = "Severe Ventriculo-Arterial Uncoupling / Cardiorenal Strain"
            coupling_status = "Substantial impedance mismatch (Ea/Ees > 1.6); progressive energetic exhaustion of myocardium."
            optimization_window = "Significantly degraded efficiency; high risk of decompensation under afterload spikes."

        return {
            "status": "success",
            "end_systolic_pressure_mmhg": round(end_systolic_pressure_mmhg, 1),
            "effective_arterial_elastance_ea": round(ea_mmhg_ml, 3),
            "end_systolic_elastance_ees": round(ees_mmhg_ml, 3),
            "ventriculo_arterial_coupling_ratio": round(vac_ratio, 3),
            "mechanical_efficiency_percentage": round(mechanical_efficiency_pct, 1),
            "stroke_volume_ml": stroke_volume_ml,
            "estimated_esv_ml": round(esv_ml, 1) if esv_ml is not None else None,
            "evaluation": {
                "classification": classification,
                "coupling_status": coupling_status,
                "optimization_window": optimization_window
            }
        }
