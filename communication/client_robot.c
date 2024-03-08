#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define MAX_BUFFER_SIZE 1024

#define LOCAL_PORT 6000

void envoiDonnees(int socket, char *buffer) {
    if (strlen(buffer) != 0) send(socket, buffer, strlen(buffer), 0);
}

void recevoirDonnees(int socket, char *buffer, int *stopBoucle) {
    ssize_t received_bytes = recv(socket, buffer, MAX_BUFFER_SIZE - 1, 0);
    if (received_bytes == -1) {
        perror("Erreur lors de la réception de données du serveur");
    } else if (received_bytes == 0) {
        printf("Le serveur a fermé la connexion\n");
        *stopBoucle = 1;
    } else {
        buffer[received_bytes] = '\0';
        printf("Message du serveur : %s\n", buffer);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <adresse IP du serveur> <port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int stopBoucle = 0;
    char bufferReception[MAX_BUFFER_SIZE];
    char bufferEmission[MAX_BUFFER_SIZE];


    const char *server_ip = argv[1];
    const int server_port = atoi(argv[2]);

    // Création de la socket
    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == -1) {
        perror("Erreur lors de la création de la socket");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse locale (choix du port local)
    struct sockaddr_in local_address;
    local_address.sin_family = AF_INET;
    local_address.sin_port = htons(LOCAL_PORT);
    local_address.sin_addr.s_addr = INADDR_ANY;

    // Attribution du port local
    if (bind(client_socket, (struct sockaddr*)&local_address, sizeof(local_address)) == -1) {
        perror("Erreur lors de l'attribution du port local");
        close(client_socket);
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse du serveur
    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(server_port);
    if (inet_pton(AF_INET, server_ip, &server_address.sin_addr) <= 0) {
        perror("Erreur lors de la conversion de l'adresse IP");
        close(client_socket);
        exit(EXIT_FAILURE);
    }

    // Connexion au serveur
    if (connect(client_socket, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) {
        perror("Erreur lors de la connexion au serveur");
        close(client_socket);
        exit(EXIT_FAILURE);
    }

    printf("Connecté au serveur %s:%d\n", server_ip, server_port);

    int compteur = 0;
    while(!stopBoucle) {
        recevoirDonnees(client_socket, bufferReception, &stopBoucle);
        if ((compteur % 2) == 0) strcpy(bufferEmission, "Bonjour, serveur!");
        else sprintf(bufferEmission, "Bonjour, serveur! Ceci est la %d-ième communication.", compteur);
        envoiDonnees(client_socket, bufferEmission);
    }

    // Fermeture de la socket
    close(client_socket);

    return 0;
}
