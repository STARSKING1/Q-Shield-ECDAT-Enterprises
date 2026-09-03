import os
import json

def test_pipeline_outputs():
    files_to_check = [
        ("cbom.json", "json"),
        ("risk_report.json", "json"),
        ("remediation_plan.json", "json"),
        ("dashboard.html", "html")
    ]
    
    print("=== Q-Shield ECDAT Pipeline Verification ===")
    all_passed = True
    
    for file_name, file_type in files_to_check:
        if not os.path.exists(file_name):
            print(f"[FAIL] Missing file: {file_name}")
            all_passed = False
            continue
        
        if os.path.getsize(file_name) == 0:
            print(f"[FAIL] Empty file: {file_name}")
            all_passed = False
            continue
            
        if file_type == "json":
            try:
                with open(file_name, "r") as f:
                    json.load(f)
                print(f"[PASS] Valid JSON artifact: {file_name}")
            except json.JSONDecodeError:
                print(f"[FAIL] Corrupted JSON file: {file_name}")
                all_passed = False
        elif file_type == "html":
            print(f"[PASS] Valid Dashboard file: {file_name}")

    if all_passed:
        print("\n[SUCCESS] All pipeline artifacts generated successfully!")
    else:
        print("\n[ERROR] Verification failed. Run 'python3 main.py' to regenerate missing files.")

if __name__ == "__main__":
    test_pipeline_outputs()
