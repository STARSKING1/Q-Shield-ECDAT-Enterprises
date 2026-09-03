import sys
from q_shield.engine.mosca import MoscaAssessment
import generate_dashboard

def main():
    print("===============================================================")
    print(" 🛡️ Q-Shield ECDAT Enterprise Post-Quantum Orchestrator ")
    print("===============================================================")
    
    # 1. Evaluate Mosca Threat Model
    mosca = MoscaAssessment(data_shelf_life_x=10.0, migration_time_y=5.0, time_to_crqc_z=8.0)
    risk_res = mosca.evaluate()
    print(f"[+] Mosca Risk Evaluated | QVI Score: {risk_res['qvi_score']} | Urgency: {risk_res['urgency']}")

    # 2. Build Dashboard
    generate_dashboard.generate()
    print("[+] Pipeline Execution Complete.")

if __name__ == "__main__":
    main()
