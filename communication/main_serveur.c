#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#include "../marvelmind/tracker.h"
#include "serveurTCP.h"

#define CHECK_INF(sts, value, msg) if ((value) < (sts)) { perror(msg); exit(EXIT_FAILURE); }

int main() {
    pid_t pid_serveurTCP, pid_simulation, pid_marvelmind;
    char *simulation = "../Simulation/v5/main.py";
    char *marvelmind = "../marvelmind/marvelmind_tracker";

    while (1) {
        // Création du processus pour le serveur TCP bidirectionnel
        pid_serveurTCP = fork();

        CHECK_INF(pid_serveurTCP, 0, "Erreur lors de la création du processus pour le serveur TCP");
        if (pid_serveurTCP == 0) {
            // Code exécuté dans le processus fils pour le serveur TCP
            printf("Lancement du serveur TCP...\n");
            serveurTCP();
            // Si serveurTCP() retourne, cela signifie qu'il y a eu une erreur
            perror("Erreur lors du lancement du serveur TCP");
            exit(EXIT_FAILURE);
        } else {
            // Code exécuté dans le processus parent
            printf("Processus fils pour le serveur TCP créé avec PID : %d\n", pid_serveurTCP);
            // Attendre un peu avant de lancer le processus suivant
            sleep(1);
        }

        // Création du processus pour le programme Python
        pid_simulation = fork();

        CHECK_INF(pid_simulation, 0, "Erreur lors de la création du processus pour le programme Python");
        if (pid_simulation == 0) {
            // Code exécuté dans le processus fils pour le programme Python
            printf("Lancement du programme Python...\n");
            execlp("python3", "python3", simulation, NULL);
            // Si execlp() retourne, cela signifie qu'il y a eu une erreur
            perror("Erreur lors du lancement du programme Python");
            exit(EXIT_FAILURE);
        } else {
            // Code exécuté dans le processus parent
            printf("Processus fils pour le programme Python créé avec PID : %d\n", pid_simulation);
            // Attendre un peu avant de recommencer la boucle
            sleep(1);
        }
        
        // Création du processus pour le programme Marvelmind
        pid_marvelmind = fork();
        
        CHECK_INF(pid_marvelmind, 0, "Erreur lors de la création du processus pour le programme Python");
        if (pid_marvelmind == 0) {
            // Code exécuté dans le processus fils pour le programme Marvelmind
            printf("Lancement du programme Marvelmind...\n");
            tracker();
            // Si tracker() retourne, cela signifie qu'il y a eu une erreur
            perror("Erreur lors du lancement du programme Marvelmind");
            exit(EXIT_FAILURE);
        } else {
            // Code exécuté dans le processus parent
            printf("Processus fils pour le programme Marvelmind créé avec PID : %d\n", pid_simulation);
            // Attendre un peu avant de recommencer la boucle
            sleep(1);
        }

        // Attente de la fin des processus fils
        wait(NULL);
        wait(NULL);
        wait(NULL);
    }

    return 0;
}

