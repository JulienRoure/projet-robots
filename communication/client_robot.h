#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

/* FONCTIONS D'ECRITURE */
void envoiDonnees(int socket, char *buffer);
void ecrireUART(char *nomProgramme);
void ecrireFichier(char *nomFichier, char *message);

/* FONCTIONS DE LECTURE */
void recevoirDonnees(int socket, char *buffer, int *stopBoucle);
void lireUART(char *nomProgramme);
void lireFichier(char* nom_fichier, char *buffer);

int client_robot(int argc, char *argv[]);

#endif /* COMMUNICATION_H */
