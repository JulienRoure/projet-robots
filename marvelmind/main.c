#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    // Créer un tube pour la communication entre les deux processus
    int pipefd[2];
    if (pipe(pipefd) == -1) {
        perror("Erreur lors de la création du tube");
        exit(EXIT_FAILURE);
    }

    // Fork pour créer le premier processus
    pid_t marvelmindPid = fork();

    if (marvelmindPid == -1) {
        perror("Erreur lors du premier fork");
        exit(EXIT_FAILURE);
    }

    if (marvelmindPid == 0) {
        // Code du processus fils (marvelmind_c)
        close(pipefd[0]);  // Fermer le côté lecture du tube

        // Rediriger la sortie standard vers le tube
        dup2(pipefd[1], STDOUT_FILENO);
        close(pipefd[1]);

        // Exécuter le programme marvelmind_c
        execl("./marvelmind_c", "marvelmind_c", NULL);

        // En cas d'échec de execl
        perror("Erreur lors de l'exécution de marvelmind_c");
        exit(EXIT_FAILURE);
    } else {
        // Fork pour créer le deuxième processus
        pid_t parserPid = fork();

        if (parserPid == -1) {
            perror("Erreur lors du deuxième fork");
            exit(EXIT_FAILURE);
        }

        if (parserPid == 0) {
            // Code du processus fils (parser)
            close(pipefd[1]);  // Fermer le côté écriture du tube

            // Rediriger l'entrée standard depuis le tube
            dup2(pipefd[0], STDIN_FILENO);
            close(pipefd[0]);

            // Exécuter le programme parser
            execl("./parser", "parser", NULL);

            // En cas d'échec de execl
            perror("Erreur lors de l'exécution de parser");
            exit(EXIT_FAILURE);
        } else {
            // Code du processus parent
            close(pipefd[0]);  // Fermer les deux côtés du tube dans le parent
            close(pipefd[1]);

            // Attendre la fin des deux processus enfants
            waitpid(marvelmindPid, NULL, 0);
            waitpid(parserPid, NULL, 0);
        }
    }

    return 0;
}
