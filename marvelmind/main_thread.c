#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h> // Pour les pipes
#include "tracker.h"
#include "parser.h"

// Structure pour passer les descripteurs de fichier à travers les threads
typedef struct {
    int input_fd;
    int output_fd;
} PipePair;

void *tracker_thread(void *arg) {
    // Cast du paramètre à PipePair
    PipePair *pipes = (PipePair *)arg;

    // Redirection de la sortie standard vers l'entrée du pipe
    dup2(pipes->output_fd, STDOUT_FILENO);

    // Fermeture du descripteur de fichier de sortie du pipe
    close(pipes->output_fd);

    // Appel de la fonction main de tracker.c
    trackerFunction();

    return NULL;
}

void *parser_thread(void *arg) {
    // Cast du paramètre à PipePair
    PipePair *pipes = (PipePair *)arg;

    // Redirection de l'entrée standard vers la sortie du pipe
    dup2(pipes->input_fd, STDIN_FILENO);

    // Fermeture du descripteur de fichier d'entrée du pipe
    close(pipes->input_fd);

    // Appel de la fonction main de parser.c
    parserFunction();

    return NULL;
}

int main() {
    pthread_t tracker_tid, parser_tid;
    PipePair pipes;

    // Création du tube (pipe)
    int pipe_fds[2];
    if (pipe(pipe_fds) == -1) {
        perror("pipe");
        return 1;
    }

    // Assignation des descripteurs de fichier aux pipes
    pipes.input_fd = pipe_fds[0];
    pipes.output_fd = pipe_fds[1];

    // Création des threads pour tracker et parser
    pthread_create(&tracker_tid, NULL, tracker_thread, &pipes);
    pthread_create(&parser_tid, NULL, parser_thread, &pipes);

    // Attente de la fin des threads
    pthread_join(tracker_tid, NULL);
    pthread_join(parser_tid, NULL);

    // Fermeture des descripteurs de fichier
    close(pipes.input_fd);
    close(pipes.output_fd);

    return 0;
}
