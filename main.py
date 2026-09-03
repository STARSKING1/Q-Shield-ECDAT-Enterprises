import json
import sys
import os
from q_shield.parsers.ast_scanner import scan_project_ast
from q_shield.models.cbom import CycloneDX16CBOM
from q_shield.engine.mosca import run_mosca_assessment
from q_shield.engine.pqc_mapper import run_pqc_mapping
from generate_dashboard import generate_html_dashboard

def run_enterprise_pipeline():
    print("============================================================")
    print(" 🛡️  Q-Shield ECDAT Enterprise Pipeline Orchestrator  🛡️ ")
    print("============================================================\n")

    # Step 1: Execute AST/CST Scanner & Generate CycloneDX 1.6 CBOM
    print("[1/5] Running AST Static Code Analysis...")
    components = scan_project_ast(".")
    cbom = CycloneDX16CBOM(
        serialNumber="urn:uuid:q-shield-cbom-production-v2",
        components=components
    )
    
    # Save CBOM artifact using Pydantic JSON dump
    with open("cbom.json", "w") as f:
        f.write(cbom.model_dump_json(indent=2) if hasattr(cbom, 'model_dump_json') else cbom.json(indent=2))
    print(f"      └── [SUCCESS] Generated cbom.json with {len(components)} discovered assets.")

    # Step 2: Run Mosca Risk Engine
    print("\n[2/5] Running Mosca Quantum Risk Engine (x + y > z)...")
    risk_report = run_mosca_assessment(data_shelf_life=10.0, migration_time=3.0, time_to_crqc=7.0)
    print(f"      └── [SUCCESS] Risk Status: {risk_report['risk_status']} (QVI Score: {risk_report['qvi_score']})")

    # Step 3: Map to NIST PQC Standards & Calculate Overhead
    print("\n[3/5] Mapping Assets to NIST FIPS 203/204/205 Standards...")
    pqc_plan = run_pqc_mapping()
    overhead = pqc_plan['aggregate_key_memory_overhead']['overall_overhead_multiplier']
    print(f"      └── [SUCCESS] Remediated {pqc_plan['total_flagged_assets']} assets. Overhead: {overhead}")

    # Step 4: Generate Interactive Executive Dashboard UI
    print("\n[4/5] Rendering High-Contrast Executive Dashboard...")
    generate_html_dashboard()
    print("      └── [SUCCESS] Dashboard compiled to dashboard.html.")

    # Step 5: Final Summary & API Readiness
    print("\n[5/5] Enterprise Pipeline Execution Complete!")
    print("============================================================")
    print(" 🚀 Artifacts Generated:")
    print("    • cbom.json              (OWASP CycloneDX 1.6 CBOM)")
    print("    • risk_report.json       (Mosca Threat Assessment)")
    print("    • remediation_plan.json  (NIST PQC Migration Roadmap)")
    print("    • dashboard.html         (Interactive UI/UX Report)")
    print("============================================================\n")

if __name__ == "__main__":
    run_enterprise_pipeline()
