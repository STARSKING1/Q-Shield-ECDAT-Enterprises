#include <vmlinux.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>

SEC("uprobe/SSL_do_handshake")
int BPF_UPROBE(trace_ssl_handshake, void *ssl) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    bpf_printk("Q-Shield eBPF: Intercepted SSL_do_handshake in PID %d\n", pid);
    return 0;
}

char LICENSE[] SEC("license") = "GPL";
