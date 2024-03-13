#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid_serveurTCP, pid_simulation;
    char *simulation = "../Simulation/v5/main.py"; //mettre ../Simulation/v5/main.py quand Tom aura push

    while (1) {
        // Création du processus pour le serveur TCP bidirectionnel
        pid_serveurTCP = fork();

        if (pid_serveurTCP < 0) {
            // Erreur lors de la création du processus
            perror("Erreur lors de la création du processus pour le serveur TCP");
            exit(EXIT_FAILURE);
        } else if (pid_serveurTCP == 0) {
            // Code exécuté dans le processus fils pour le serveur TCP
            printf("Lancement du serveur TCP...\n");
            execl("./serveurTCP_bidiric", "serveurTCP_bidiric", NULL);
            // Si execl() retourne, cela signifie qu'il y a eu une erreur
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

        if (pid_simulation < 0) {
            // Erreur lors de la création du processus
            perror("Erreur lors de la création du processus pour le programme Python");
            exit(EXIT_FAILURE);
        } else if (pid_simulation == 0) {
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

        // Attente de la fin des processus fils
        wait(NULL);
        wait(NULL);
    }

    return 0;
}

