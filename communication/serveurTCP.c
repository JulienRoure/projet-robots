#include "serveurTCP.h"

#define MAX_BUFFER_SIZE 1024
#define LOCALIP "127.0.0.1"
#define LOCALPORT 3000
#define NB_MAX_CONNECTIONS 3

#define CHECKERROR(var,val,msg)     if (var==val) {perror(msg); exit(EXIT_FAILURE);}
#define CHECKERROR_SOCK(var,val,msg, socket)     if (var==val) {perror(msg); close(socket); exit(EXIT_FAILURE);}

void ecrireFichier(char *nomFichier, char *message) {
    FILE *fichier = fopen(nomFichier, "w");
    if (fichier == NULL) {
        perror("Erreur lors de l'ouverture du fichier.\n");
        exit(1);
    }
    int ret = fprintf(fichier, "%s\n", message);
    if (ret < 0) {
        perror(("Erreur lors de l'écriture dans le fichier %s\n", nomFichier));
        exit(EXIT_FAILURE);
    }
    fclose(fichier);
}

void lireFichier(char* nomFichier, char *buffer) {
    FILE* fichier;
    long taille_fichier;
    
    fichier = fopen(nomFichier, "r");
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
        //printf("Message reçu sur la socket n°%d ; ", socket);
        //printf("Message du client : %s\n", bufferEmission);
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

void attendre_secondes(int secondesAttente) {
	sleep(secondesAttente);
}

int serveurTCP() {
    int socketEcoute, socketDialogue[NB_MAX_CONNECTIONS];
    struct sockaddr_in serverAddr, clientAddr[NB_MAX_CONNECTIONS];
    socklen_t addrSize = sizeof(struct sockaddr_in);
	
	char fichierCommande[MAX_BUFFER_SIZE][NB_MAX_CONNECTIONS]; //Tableau contenant les fichiers avec commandes A ENVOYER aux robots
	char etatsRobots[MAX_BUFFER_SIZE][NB_MAX_CONNECTIONS]; //Tableau contenant les fichiers avec les états des robots RECUs des robots
	
	char previousBufferEmission[MAX_BUFFER_SIZE];
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
		
		sprintf(fichierCommande[i], "../Simulation/v5/fichiers_ecriture/robot_target%d.txt", i);
		sprintf(etatsRobots[i], "../Simulation/v5/fichiers_lecture/etat_robot%d.txt", i);
		
		ecrireFichier(etatsRobots[i], "0"); // On initialise la valeur contenue dans "etat_robot#.txt"
    	
        // Création des sockets
        socketDialogue[i] = accept(socketEcoute, (struct sockaddr*)&(clientAddr[i]), &addrSize);
        // On coupe toutes les connections si une seule échoue! Comportement à modifier?
        CHECKERROR_SOCK(socketDialogue[i],-1, "Erreur lors de l'acceptation de la connexion\n", socketEcoute);
        printf("Connexion acceptée depuis %s:%d\n", inet_ntoa(clientAddr[i].sin_addr), ntohs(clientAddr[i].sin_port));

        // Création des processus fils
        pidFils[i] = fork(); // Faut-il déclarer pidFils[] comme variable globale? à vérifier

        if (pidFils[i] == 0) {
            // On est dans le fils
            printf("Je suis le processus fils %d, j'ai été créé en %d-ième.\n", getpid(), i);
            printf("Je suis connecté au client ayant l'adresse IP:Port %s:%d\n", inet_ntoa(clientAddr[i].sin_addr), ntohs(clientAddr[i].sin_port));

            // Indiquer au client son identifiant
            sprintf(bufferEmission, "Tu es le robot %d", i);
            send(socketDialogue[i], bufferEmission, strlen(bufferEmission), 0);
            attendre_secondes(2);
            
            
            /* -------------------------------------------- */
			/* ----- BOUCLE D'ACTION LECTURE/ECRITURE ----- */
			/* -------------------------------------------- */
            
			while(1) {
		        
		        printf("----------------------\n");
		        
		        //Envoyer les commandes
		        lireFichier(fichierCommande[i], bufferEmission);
		    	send(socketDialogue[i], bufferEmission, strlen(bufferEmission), 0);
		    	printf("Envoi de la commande = %s au robot n°%d.\n", bufferEmission, i);
		    	
		    	//Reception de l'état du robot
		        recevoirDonnees(socketDialogue[i], bufferReception, NULL);
		        if (bufferReception[0] == '1'){
		        	ecrireFichier(etatsRobots[i], bufferReception);
		        	printf("Reçu : %s. Le robot n°%d est arrivé !\n", bufferReception, i);
		        }
		        else{
		        	printf("Reçu : %s. Le robot n°%d n'est pas encore arrivé.\n", bufferReception, i);
		        }
		        
		        //attendre_XXns(50000000); // Odg : attendre 50ms entre deux envois pour pouvoir les distinguer chez le client
		        attendre_secondes(5); //attendre 5 secondes
	        }
	        
	        /* -------------------------------------------- */
			/* -------------------------------------------- */
			/* -------------------------------------------- */

            
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
