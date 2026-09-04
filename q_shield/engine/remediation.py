import os
from q_shield.parsers.refactor import refactor_code

class BatchRemediator:
    @staticmethod
    def remediate_path(target_path: str) -> dict:
        results = {}
        if os.path.isfile(target_path):
            files = [target_path]
        else:
            files = [os.path.join(root, file) for root, _, filenames in os.walk(target_path) for file in filenames if file.endswith('.py')]

        for filepath in files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                updated_content = refactor_code(content)
                if updated_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    results[filepath] = "Refactored successfully"
                else:
                    results[filepath] = "No vulnerable primitives matched"
            except Exception as e:
                results[filepath] = f"Error: {str(e)}"
        return results
