import os
from typing import List, Dict, Any

def scan_codebase_cst(target_dir: str = ".") -> List[Dict[str, Any]]:
    findings = []
    
    try:
        from tree_sitter import Language, Parser
        import tree_sitter_python as tspy
        import tree_sitter_c as tsc

        # Initialize Languages
        PY_LANG = Language(tspy.language())
        C_LANG = Language(tsc.language())

        py_parser = Parser(PY_LANG)
        c_parser = Parser(C_LANG)

        for root, _, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if "site-packages" in file_path or ".git" in file_path:
                    continue

                if file.endswith(".py"):
                    with open(file_path, "rb") as f:
                        tree = py_parser.parse(f.read())
                        query = PY_LANG.query("""
                            (call function: (attribute) @func (#match? @func "RSA|ECDSA|sha1|md5"))
                        """)
                        for match in query.matches(tree.root_node):
                            findings.append({
                                "file": file_path,
                                "type": "Python AST Call",
                                "node": str(match)
                            })

                elif file.endswith(".c") or file.endswith(".h"):
                    with open(file_path, "rb") as f:
                        tree = c_parser.parse(f.read())
                        query = C_LANG.query("""
                            (call_expression function: (identifier) @func (#match? @func "RSA_|EVP_PKEY_|SSL_"))
                        """)
                        for match in query.matches(tree.root_node):
                            findings.append({
                                "file": file_path,
                                "type": "Native C Call",
                                "node": str(match)
                            })

    except ImportError as e:
        print(f"[!] Tree-sitter fallback mode: {e}")
    
    return findings

if __name__ == "__main__":
    results = scan_codebase_cst(".")
    print(f"[+] Tree-Sitter CST Discovery Complete: Flagged {len(results)} native/python crypto nodes.")
