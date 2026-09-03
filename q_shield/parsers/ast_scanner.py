import ast
import os
from typing import List
from q_shield.models.cbom import (
    CBOMComponent, CryptoProperties, AlgorithmProperties, PrimitiveType
)

class CryptoASTVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.components: List[CBOMComponent] = []
        self._count = 0

    def visit_Import(self, node):
        for alias in node.names:
            self._check_name(alias.name, node.lineno)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        for alias in node.names:
            full_name = f"{module}.{alias.name}" if module else alias.name
            self._check_name(full_name, node.lineno)
        self.generic_visit(node)

    def visit_Call(self, node):
        func_name = ""
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id

        if func_name.lower() in ["sha1", "md5"]:
            self._add_component(
                name=func_name.upper(),
                primitive=PrimitiveType.HASH,
                sec_level=0,
                line=node.lineno
            )
        self.generic_visit(node)

    def _check_name(self, name: str, line: int):
        u = name.upper()
        if "RSA" in u:
            self._add_component("RSA-2048", PrimitiveType.ASYMMETRIC, 112, line)
        elif "ECC" in u or "ECDSA" in u:
            self._add_component("ECDSA-P256", PrimitiveType.ASYMMETRIC, 128, line)
        elif "AES" in u:
            self._add_component("AES-128", PrimitiveType.SYMMETRIC, 128, line)

    def _add_component(self, name: str, primitive: PrimitiveType, sec_level: int, line: int):
        self._count += 1
        comp = CBOMComponent(
            name=name,
            bom_ref=f"cbom-ref-{self.file_path}-{line}-{self._count}",
            cryptoProperties=CryptoProperties(
                algorithmProperties=AlgorithmProperties(
                    primitive=primitive,
                    classicalSecurityLevel=sec_level,
                    nistQuantumSecurityLevel=0
                )
            ),
            evidence={"file": self.file_path, "line": line}
        )
        self.components.append(comp)

def scan_project_ast(target_dir: str = ".") -> List[CBOMComponent]:
    results = []
    ignore_dirs = {".git", "__pycache__", ".venv", "env"}
    
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=full_path)
                    visitor = CryptoASTVisitor(full_path)
                    visitor.visit(tree)
                    results.extend(visitor.components)
                except Exception:
                    continue
    return results
