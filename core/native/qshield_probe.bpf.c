#define __TARGET_ARCH_arm64
typedef unsigned int u32;
typedef unsigned long long u64;

#define SEC(name) __attribute__((section(name), used))

SEC("uprobe/SSL_do_handshake")
int trace_ssl_handshake(void *ctx) {
    return 0;
}

char LICENSE[] SEC("license") = "GPL";
