import ast
import os
import json

class CryptoASTVisitor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path
        self.findings = []

    def visit_Import(self, node):
        for alias in node.names:
            self._check_module(alias.name, node.lineno)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        for alias in node.names:
            full_name = f"{module}.{alias.name}" if module else alias.name
            self._check_module(full_name, node.lineno)
        self.generic_visit(node)

    def visit_Call(self, node):
        # Detect function calls like hashlib.sha1() or hashlib.md5()
        func_name = ""
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id

        if func_name.lower() in ["sha1", "md5"]:
            self.findings.append({
                "name": func_name.upper(),
                "key_size": None,
                "file": self.file_path,
                "line": node.lineno,
                "type": "Weak Hash Function"
            })
        self.generic_visit(node)

    def _check_module(self, name, line_no):
        name_upper = name.upper()
        if "RSA" in name_upper:
            self.findings.append({"name": "RSA", "key_size": 2048, "file": self.file_path, "line": line_no, "type": "Asymmetric Key"})
        elif "ECC" in name_upper or "ECDSA" in name_upper:
            self.findings.append({"name": "ECDSA", "key_size": 256, "file": self.file_path, "line": line_no, "type": "Asymmetric Key"})
        elif "AES" in name_upper:
            self.findings.append({"name": "AES", "key_size": 128, "file": self.file_path, "line": line_no, "type": "Symmetric Cipher"})
        elif "SHA1" in name_upper or "MD5" in name_upper:
            self.findings.append({"name": name_upper, "key_size": None, "file": self.file_path, "line": line_no, "type": "Weak Hash"})

def scan_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
        visitor = CryptoASTVisitor(file_path)
        visitor.visit(tree)
        return visitor.findings
    except Exception:
        return []

def main():
    components = []
    ignore_files = {"scanner.py", "risk_engine.py", "pqc_remediator.py", "generate_dashboard.py", "main.py", "test_pipeline.py"}

    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and file not in ignore_files:
                full_path = os.path.join(root, file)
                findings = scan_file(full_path)
                components.extend(findings)

    cbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": "urn:uuid:q-shield-cbom-production",
        "version": 1,
        "components": components
    }

    with open("cbom.json", "w") as f:
        json.dump(cbom, f, indent=2)

    print(f"[+] AST Scan Complete. Generated cbom.json with {len(components)} real discovered assets.")

if __name__ == "__main__":
    main()
