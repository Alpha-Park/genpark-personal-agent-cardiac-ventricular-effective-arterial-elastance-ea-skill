# Cardiac Ventricular Effective Arterial Elastance (Ea) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Ventriculo-Arterial Coupling ($E_a / E_{es}$) and Effective Arterial Elastance ($E_a$) Analyzer based on pressure-volume loop physics.

```mermaid
flowchart TD
    A[Systolic Blood Pressure & Stroke Volume] --> B[Estimate End-Systolic Pressure ESP = 0.9 * SBP]
    B & A --> C[Effective Arterial Elastance: Ea = ESP / SV]
    D[LVEF or Systolic Time Intervals] --> E[End-Systolic Elastance Ees]
    C & E --> F[Ventriculo-Arterial Coupling Ratio: Ea / Ees]
    F --> G[Mechanical Stroke Work Efficiency & Afterload Guidance]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Pressure-Volume Framework**: Single-beat validated elastance and coupling models.
- **Cardiovascular Energetics**: Direct computation of stroke work mechanical efficiency.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
