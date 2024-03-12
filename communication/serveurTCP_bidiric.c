#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#include <time.h>

#include <sys/types.h>
#include <sys/wait.h>

#define MAX_BUFFER_SIZE 1024
#define LOCALIP "127.0.0.1"
#define LOCALPORT 3000
#define READER_PORT 5000 // Serveur = lecteur, client = écrivain
#define WRITER_PORT 5001 // Serveur = écrivain, client = lecteur

#define NB_MAX_CONNECTIONS 1

#define CHECKERROR(var,val,msg)     if (var==val) {perror(msg); exit(EXIT_FAILURE);}

#define CHECKERROR_SOCK(var,val,msg, socket)     if (var==val) {perror(msg); close(socket); exit(EXIT_FAILURE);}

void ecrireFichier(char *message, char *nom_fichier) {
    FILE *fichier = fopen(nom_fichier, "a");
    if (fichier == NULL) {
        perror("Erreur lors de l'ouverture du fichier");
        exit(1);
    }
    fprintf(fichier, "%s\n", message);
    fclose(fichier);
}

void lireFichier(char* nom_fichier, char *buffer) {
    FILE* fichier;
    // char* buffer = NULL;
    long taille_fichier;
    
    fichier = fopen(nom_fichier, "r");
    if (fichier == NULL) {
        printf("Le fichier spécifié n'existe pas.\n");
        return;
    }
    
    fseek(fichier, 0, SEEK_END);
    taille_fichier = ftell(fichier);
    rewind(fichier);
    
    // buffer = (char*)malloc(taille_fichier * sizeof(char));
    if (buffer == NULL) {
        printf("lireFichier : Erreur d'allocation de mémoire.\n");
        fclose(fichier);
        return;
    }
    
    fread(buffer, sizeof(char), taille_fichier, fichier);
    fclose(fichier);
    buffer[taille_fichier] = '\0';
    
    return;
}

void recevoirDonnees(int socket, char *bufferEmission, int *stopBoucle) {
    ssize_t received_bytes = recv(socket, bufferEmission, MAX_BUFFER_SIZE - 1, 0);
    if (received_bytes == -1) {
        perror("Erreur lors de la réception de données du client");
    } else if (received_bytes == 0) {
        printf("Le client a fermé la connexion\n");
        *stopBoucle = 1;
    } else {
        bufferEmission[received_bytes] = '\0';
        printf("Message reçu sur la socket n°%d ; ", socket);
        printf("Message du client : %s\n", bufferEmission);
    }
}

void attendre_XXns(int nsAttente) {
    struct timespec attente;
    attente.tv_sec = 0;
    attente.tv_nsec = nsAttente;

    if (nanosleep(&attente, NULL) == -1) {
        perror("Erreur lors de l'attente");
    }
}

int main() {
    int socketEcoute, socketDialogue[NB_MAX_CONNECTIONS];
    struct sockaddr_in serverAddr, clientAddr[NB_MAX_CONNECTIONS];
    socklen_t addrSize = sizeof(struct sockaddr_in);
	
	char fichierCommande[MAX_BUFFER_SIZE][NB_MAX_CONNECTIONS];
	
    char bufferEmission[MAX_BUFFER_SIZE];
    char bufferReception[MAX_BUFFER_SIZE];
    pid_t pidFils[NB_MAX_CONNECTIONS]; //Permet de recuperer le pid du processus fils créé

    // Créer une socket
    socketEcoute = socket(AF_INET, SOCK_STREAM, 0);
    if (socketEcoute == -1) {
        perror("Erreur lors de la création de la socket");
        exit(EXIT_FAILURE);
    }

    // Configuration de l'adresse du serveur
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(LOCALPORT);

    // Liaison de la socket à l'adresse
    if (bind(socketEcoute, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == -1) {
        perror("Erreur lors de la liaison de la socket");
        close(socketEcoute);
        exit(EXIT_FAILURE);
    }

    // Mettre la socket en mode écoute
    if (listen(socketEcoute, NB_MAX_CONNECTIONS) == -1) {
        perror("Erreur lors de la mise en écoute de la socket");
        close(socketEcoute);
        exit(EXIT_FAILURE);
    }

    printf("En attente de connexions...\n");
    

    // Création des processus et sockets client
    for(int i = 0; i < NB_MAX_CONNECTIONS; i++) {
		
		sprintf(fichierCommande[i], "robot_target%d.txt", i);
		// printf("fichierCommande[i] = %s\n", fichierCommande[i]);
    	
        // Création des sockets
        socketDialogue[i] = accept(socketEcoute, (struct sockaddr*)&(clientAddr[i]), &addrSize);
        CHECKERROR_SOCK(socketDialogue[i],-1, "Erreur lors de l'acceptation de la connexion\n", socketEcoute); // On coupe toutes les connections si une seule échoue! Comportement à modifier?
        printf("Connexion acceptée depuis %s:%d\n", inet_ntoa(clientAddr[i].sin_addr), ntohs(clientAddr[i].sin_port));

        // Création des processus fils
        pidFils[i] = fork(); // Faut-il déclarer pidFils[] comme variable globale? à vérifier

        if (pidFils[i] == 0) {
            // On est dans le fils
            printf("Je suis le processus fils %d, j'ai été créé en %d-ième.\n", getpid(), i + 1);
            printf("Je suis connecté au client ayant l'adresse IP:Port %s:%d\n", inet_ntoa(clientAddr[i].sin_addr), ntohs(clientAddr[i].sin_port));

            // Indiquer au client son identifiant
            sprintf(bufferEmission, "Tu es le robot %d", i);
            send(socketDialogue[i], bufferEmission, strlen(bufferEmission), 0);
            
			while(1) {    
		        //sprintf(bufferEmission, "Message n°%d adressé au client n°%d\n", j, i);
		        //send(socketDialogue[i], bufferEmission, strlen(bufferEmission), 0);
		        lireFichier(fichierCommande[i], bufferEmission);
                printf("bufferEmission = %s\n", bufferEmission);
		    	send(socketDialogue[i], bufferEmission, strlen(bufferEmission), 0);
		        recevoirDonnees(socketDialogue[i], bufferReception, NULL);
		        attendre_XXns(50000000); // Odg : attendre 50ms entre deux envois pour pouvoir les distinguer chez le client 
	        }

            
            // sleep(10);
            // printf("Après le wait\n");
            exit(EXIT_SUCCESS);
        } else {
            // On est dans le processus père
            // close(socketDialogue[i]); //fermeture des sockets de dialogue utilisées par le père (possédée par le fils désormais)
        }
    }
    
    // Reste du code exécuté par le père
    for (int i = 0; i < NB_MAX_CONNECTIONS; i++) wait(NULL); // Attends que chaque processus fils se termine

    // Fermer les sockets
    for (int i = 0; i < NB_MAX_CONNECTIONS; i++) close(socketDialogue[i]);
    close(socketEcoute);

    return 0;
}
