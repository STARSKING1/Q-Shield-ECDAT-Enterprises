import subprocess
import sys
import time

def run_step(step_name, command):
    print(f"\n[+] Running {step_name}...")
    start_time = time.time()
    result = subprocess.run(command, shell=True)
    elapsed = time.time() - start_time
    if result.returncode != 0:
        print(f"[!] Step failed: {step_name}. Execution stopped.")
        sys.exit(1)
    print(f"[✔] Completed {step_name} ({elapsed:.2f}s)")

def main():
    print("==================================================")
    print("   🛡️ Q-SHIELD ECDAT: QUANTUM MIGRATION TOOLKIT    ")
    print("==================================================")

    run_step("Module 1 & 2: AST Scan & CBOM Generation", "python3 scanner.py")
    run_step("Module 3: Quantum Risk Assessment & Mosca Engine", "python3 risk_engine.py")
    run_step("Module 4: NIST PQC & Hybrid Remediation Mapper", "python3 pqc_remediator.py")
    run_step("Module 5: Executive Dashboard Generation", "python3 generate_dashboard.py")

    print("\n==================================================")
    print("   SUCCESS: All pipeline modules executed!        ")
    print("   View dashboard at: http://localhost:8081/dashboard.html")
    print("==================================================")

if __name__ == "__main__":
    main()
