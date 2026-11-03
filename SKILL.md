---
name: genpark-personal-agent-cardiac-ventricular-effective-arterial-elastance-ea-skill
description: Effective Arterial Elastance (Ea) and End-Systolic Elastance (Ees) ventriculo-arterial coupling analyzer. Computes Ea = ESP / SV, energetic coupling ratio Ea / Ees, and stroke work efficiency.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - cardiology
  - elastance
  - afterload
  - ventriculo-arterial-coupling
  - openclaw
  - genpark
  - mcp
---

# Cardiac Ventricular Effective Arterial Elastance (Ea) Skill

## Overview
This skill computes ventriculo-arterial coupling (VAC) metrics based on pressure-volume framework principles:
- **Effective Arterial Elastance ($E_a$)**: Integrates peripheral vascular resistance, systemic arterial compliance, characteristic impedance, and heart rate into a single afterload parameter.
- **Left Ventricular End-Systolic Elastance ($E_{es}$)**: Represents chamber contractility and end-systolic stiffness.
- **Ventriculo-Arterial Coupling ($E_a / E_{es}$)**: Optimal cardiac stroke work transfer occurs at a ratio near 1.0, while maximal metabolic myocardial oxygen efficiency occurs at 0.5 to 0.7.

## Mathematical Formulation
1. **End-Systolic Pressure (ESP)**:
   $$\text{ESP} = 0.90 \times \text{SBP}$$
2. **Effective Arterial Elastance**:
   $$E_a = \frac{\text{ESP}}{\text{Stroke Volume (mL)}}$$
3. **End-Systolic Elastance**:
   $$E_{es} = \frac{\text{ESP}}{\text{ESV}} = E_a \times \frac{\text{LVEF}}{1 - \text{LVEF}}$$
4. **Ventriculo-Arterial Coupling Ratio**:
   $$\text{VAC} = \frac{E_a}{E_{es}}$$
5. **Mechanical Work Efficiency**:
   $$\eta = \frac{1}{1 + 0.5 \times \text{VAC}} \times 100\%$$

## Usage
```python
from client import VentriculoArterialCouplingClient

client = VentriculoArterialCouplingClient()
res = client.evaluate_coupling(
    systolic_bp_mmhg=120.0,
    diastolic_bp_mmhg=80.0,
    stroke_volume_ml=70.0,
    left_ventricular_ejection_fraction=0.60
)
print(res["evaluation"]["classification"])
```
