#include <fcntl.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

/*
 * Spelunk: A baby's first pwn challenge.
 *
 * Instructions:
 * - Compiled as 32-bit x86.
 * - No stack protection, no PIE, executable stack.
 * - The flag is opened at the start of the program and its FD is kept open.
 * - The goal is to inject shellcode that reads from the flag's FD and writes to
 * stdout.
 */

void vuln(int client_fd) {
  char buf[128];

  // Redirect stdin and stdout to the client socket
  dup2(client_fd, 0);
  dup2(client_fd, 1);

  // Leak the buffer address to make it easy to jump to shellcode
  printf(
      "Hello adventurer! I've found a secret cave, but I've lost my light.\n");
  printf("I can see my map at: %p\n", (void *)buf);
  printf("Can you help me? What did you find? ");
  fflush(stdout);

  // The vulnerability: gets() reads until newline, allowing buffer overflow.
  gets(buf);

  printf("You found: %s\n", buf);
  printf("That doesn't seem to help... goodbye!\n");
  fflush(stdout);
}

int main() {
  // 1. Open flag file. This will likely be FD 3.
  // The entrypoint script will write this file and then delete it after 1
  // second.
  int flag_fd = open("/tmp/flag.txt", O_RDONLY);
  if (flag_fd == -1) {
    perror("Error opening flag");
    exit(1);
  }

  // 2. Setup socket server on port 1337
  int server_fd = socket(AF_INET, SOCK_STREAM, 0);
  if (server_fd == -1) {
    perror("socket");
    exit(1);
  }

  int opt = 1;
  if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) ==
      -1) {
    perror("setsockopt");
    exit(1);
  }

  struct sockaddr_in addr;
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = INADDR_ANY;
  addr.sin_port = htons(1337);

  if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
    perror("bind");
    exit(1);
  }

  if (listen(server_fd, 5) == -1) {
    perror("listen");
    exit(1);
  }

  printf("Spelunk is waiting for explorers on port 1337...\n");

  while (1) {
    int client_fd = accept(server_fd, NULL, NULL);
    if (client_fd == -1) {
      perror("accept");
      continue;
    }

    pid_t pid = fork();
    if (pid == 0) {
      // Child process handles the connection
      close(server_fd);
      vuln(client_fd);
      close(client_fd);
      exit(0);
    } else if (pid < 0) {
      perror("fork");
    }

    // Parent process continues to listen
    close(client_fd);
  }

  return 0;
}
