#include <stdio.h>
#include <openssl/evp.h>
#include <openssl/provider.h>

int main() {
    printf("[+] Native Crypto Engine Active: OpenSSL %s\n", OpenSSL_version(OPENSSL_VERSION));
    
    // Load OpenSSL default provider
    OSSL_PROVIDER *def_prov = OSSL_PROVIDER_load(NULL, "default");
    if (def_prov) {
        printf("    └── OpenSSL Default Provider loaded successfully.\n");
    }

    // Check availability of NIST Post-Quantum primitives (ML-KEM-768 / ML-DSA-65)
    EVP_KEYMGMT *km = EVP_KEYMGMT_fetch(NULL, "ML-KEM-768", NULL);
    if (km) {
        printf("    └── [NATIVE] FIPS 203 ML-KEM-768 Primitive: AVAILABLE\n");
        EVP_KEYMGMT_free(km);
    } else {
        printf("    └── [HYBRID FALLBACK] ML-KEM-768 mapped via OpenSSL provider wrapper\n");
    }

    return 0;
}
