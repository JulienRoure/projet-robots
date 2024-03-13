#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "parser.h"

int parserFunction() {
    char buffer[1000];

    // Lire chaque ligne de l'entrée standard (peut être modifié selon votre source de données)
    while (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        // Vérifier si la ligne contient "Stationary beacon"
        if (strstr(buffer, "Stationary beacon") == NULL) {
            // Si la ligne ne contient pas "Stationary beacon", alors c'est une ligne à analyser
            int address;
            float x, y;

            // Utiliser sscanf pour extraire les valeurs nécessaires
            if (sscanf(buffer, "Address: %d, X: %f, Y: %f", &address, &x, &y) == 3) {
                // Afficher les valeurs extraites
                printf("Address: %d, X: %.3f, Y: %.3f\n", address, x, y);
            }
        }
    }

    return 0;
}

int main(void) {
    parserFunction();
    return 0;
}