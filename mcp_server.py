"""
MCP Server for Cardiac Ventriculo-Arterial Coupling (Ea/Ees) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import VentriculoArterialCouplingClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-cardiac-ventricular-effective-arterial-elastance-ea-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_coupling",
                        "description": "Calculate Effective Arterial Elastance (Ea), End-Systolic Elastance (Ees), and Ventriculo-Arterial Coupling (Ea/Ees).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "systolic_bp_mmhg": {"type": "number", "description": "Systolic BP (mmHg)."},
                                "diastolic_bp_mmhg": {"type": "number", "description": "Diastolic BP (mmHg)."},
                                "stroke_volume_ml": {"type": "number", "description": "Stroke volume in mL."},
                                "pre_ejection_period_ms": {"type": "number", "description": "PEP in ms (default: 80.0)."},
                                "total_ejection_time_ms": {"type": "number", "description": "LVET in ms (default: 300.0)."},
                                "left_ventricular_ejection_fraction": {"type": "number", "description": "LVEF fraction (e.g. 0.60, optional)."}
                            },
                            "required": ["systolic_bp_mmhg", "diastolic_bp_mmhg", "stroke_volume_ml"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_coupling":
            client = VentriculoArterialCouplingClient()
            try:
                res = client.evaluate_coupling(
                    systolic_bp_mmhg=float(args["systolic_bp_mmhg"]),
                    diastolic_bp_mmhg=float(args["diastolic_bp_mmhg"]),
                    stroke_volume_ml=float(args["stroke_volume_ml"]),
                    pre_ejection_period_ms=float(args.get("pre_ejection_period_ms", 80.0)),
                    total_ejection_time_ms=float(args.get("total_ejection_time_ms", 300.0)),
                    left_ventricular_ejection_fraction=float(args["left_ventricular_ejection_fraction"]) if "left_ventricular_ejection_fraction" in args and args["left_ventricular_ejection_fraction"] is not None else None
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
