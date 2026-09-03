from typing import Dict, Any

try:
    import libcst as cst
    from libcst import matchers as m

    class CryptoRefactorTransformer(cst.CSTTransformer):
        def __init__(self):
            super().__init__()
            self.modifications_count = 0

        def leave_ImportFrom(self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom) -> cst.ImportFrom:
            if m.matches(original_node.module, m.Attribute(value=m.Name("Crypto"), attr=m.Name("PublicKey"))):
                self.modifications_count += 1
                return updated_node.with_changes(
                    module=cst.parse_expression("q_shield.pqc_crypto"),
                    names=[cst.ImportAlias(name=cst.Name("HybridMLKEM768"))]
                )
            return updated_node

        def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
            if m.matches(original_node.func, m.Attribute(value=m.Name("RSA"), attr=m.Name("generate"))):
                self.modifications_count += 1
                return cst.Call(
                    func=cst.parse_expression("HybridMLKEM768.generate_keypair"),
                    args=[]
                )
            return updated_node

    def remediate_code_string(code_content: str) -> Dict[str, Any]:
        try:
            source_tree = cst.parse_module(code_content)
            transformer = CryptoRefactorTransformer()
            modified_tree = source_tree.visit(transformer)
            return {
                "success": True,
                "modifications": transformer.modifications_count,
                "remediated_code": modified_tree.code
            }
        except Exception as e:
            return {"success": False, "error": str(e), "remediated_code": code_content}

except ImportError:
    # Pure Python Regex Fallback Engine if libcst is unavailable
    import re

    def remediate_code_string(code_content: str) -> Dict[str, Any]:
        modified = code_content
        mods = 0
        if "from Crypto.PublicKey import RSA" in modified:
            modified = modified.replace("from Crypto.PublicKey import RSA", "from q_shield.pqc_crypto import HybridMLKEM768")
            mods += 1
        if "RSA.generate(2048)" in modified:
            modified = modified.replace("RSA.generate(2048)", "HybridMLKEM768.generate_keypair()")
            mods += 1
            
        return {
            "success": True,
            "modifications": mods,
            "remediated_code": modified
        }
