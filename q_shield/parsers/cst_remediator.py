from typing import Tuple
import libcst as cst
from libcst import matchers as m


class PQCRemediator(cst.CSTTransformer):
    def __init__(self):
        super().__init__()
        self.transformations_applied = 0

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.ImportFrom:
        if m.matches(
            original_node,
            m.ImportFrom(
                module=m.Attribute(value=m.Name("Crypto"), attr=m.Name("PublicKey"))
            ),
        ):
            self.transformations_applied += 1
            return updated_node.with_changes(
                module=cst.parse_expression("q_shield.crypto.pqc_provider")
            )
        return updated_node

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if m.matches(
            original_node,
            m.Call(
                func=m.Attribute(value=m.Name("RSA"), attr=m.Name("generate"))
            ),
        ):
            self.transformations_applied += 1
            return cst.Call(
                func=cst.parse_expression("QuantumSafeProvider.generate_mlkem_keypair"),
                args=[],
            )

        if m.matches(
            original_node,
            m.Call(
                func=m.Attribute(value=m.Name("ECC"), attr=m.Name("generate"))
            ),
        ):
            self.transformations_applied += 1
            return cst.Call(
                func=cst.parse_expression("QuantumSafeProvider.generate_mldsa_keypair"),
                args=[],
            )

        return updated_node


def remediate_code(source_code: str) -> Tuple[str, int]:
    if not source_code or not source_code.strip():
        return source_code, 0
    try:
        tree = cst.parse_module(source_code)
        transformer = PQCRemediator()
        modified_tree = tree.visit(transformer)
        return modified_tree.code, transformer.transformations_applied
    except Exception:
        return source_code, 0
