#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/uio.h>
#include <unistd.h>
#include <string.h>

int scan_process_memory(pid_t pid, void *remote_addr, size_t size) {
    char buffer[4096];
    struct iovec local[1];
    struct iovec remote[1];

    local[0].iov_base = buffer;
    local[0].iov_len = sizeof(buffer);
    remote[0].iov_base = remote_addr;
    remote[0].iov_len = size;

    // Direct process_vm_readv syscall execution
    ssize_t bytes_read = process_vm_readv(pid, local, 1, remote, 1, 0);
    if (bytes_read > 0) {
        if (memmem(buffer, bytes_read, "-----BEGIN RSA PRIVATE KEY-----", 31)) {
            printf("[CRITICAL] Unencrypted RSA key found in PID %d heap!\n", pid);
            return 1;
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <PID>\n", argv[0]);
        return 0;
    }
    pid_t pid = atoi(argv[1]);
    printf("[+] Initiating native process_vm_readv scan on PID %d...\n", pid);
    scan_process_memory(pid, (void*)0x555555554000, 4096);
    return 0;
}
