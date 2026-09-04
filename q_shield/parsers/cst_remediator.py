import libcst as cst
from libcst import matchers as m

class PQCRemediator(cst.CSTTransformer):
    """
    Transforms legacy pycryptodome / cryptography imports into
    q_shield post-quantum hybrid wrappers via CST manipulation.
    """
    def __init__(self):
        super().__init__()
        self.transformations_applied = 0

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.ImportFrom:
        # Match 'from Crypto.PublicKey import RSA'
        if m.matches(
            original_node,
            m.ImportFrom(
                module=m.Attribute(value=m.Name("Crypto"), attr=m.Name("PublicKey"))
            )
        ):
            self.transformations_applied += 1
            return updated_node.with_changes(
                module=cst.Attribute(
                    value=cst.Name("q_shield"),
                    attr=cst.Name("pqc")
                ),
                names=[
                    cst.ImportAlias(name=cst.Name("HybridMLKEM768")),
                    cst.ImportAlias(name=cst.Name("MLDSA65"))
                ]
            )
        
        # Match 'from cryptography.hazmat.primitives.asymmetric import rsa'
        if m.matches(
            original_node,
            m.ImportFrom(
                module=m.Attribute(
                    value=m.Attribute(
                        value=m.Attribute(value=m.Name("cryptography"), attr=m.Name("hazmat")),
                        attr=m.Name("primitives")
                    ),
                    attr=m.Name("asymmetric")
                )
            )
        ):
            self.transformations_applied += 1
            return updated_node.with_changes(
                module=cst.Attribute(
                    value=cst.Name("q_shield"),
                    attr=cst.Name("pqc")
                ),
                names=[cst.ImportAlias(name=cst.Name("FIPS203_MLKEM"))]
            )

        return updated_node

def remediate_code(source_code: str) -> tuple[str, int]:
    wrapper = cst.MetadataWrapper(cst.parse_module(source_code))
    transformer = PQCRemediator()
    modified_tree = wrapper.visit(transformer)
    return modified_tree.code, transformer.transformations_applied
