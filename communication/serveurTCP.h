#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <time.h>

void ecrireFichier(char *nomFichier, char *message);
void lireFichier(char* nomFichier, char *buffer);
void recevoirDonnees(int socket, char *bufferEmission, int *stopBoucle);
void attendre_XXns(int nsAttente);
void attendre_secondes(int secondesAttente);

int serveurTCP();

#endif /* COMMUNICATION_H */
