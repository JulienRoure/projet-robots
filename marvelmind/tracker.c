#include "tracker.h"

#define CHECK(sts, value, msg)             \
    if ((value) == (sts)) { perror(msg); exit(EXIT_FAILURE); }

bool terminateProgram=false;

void CtrlHandler(int signum) {
    terminateProgram=true;
}

static sem_t *sem;
struct timespec ts;
void semCallback() {
	sem_post(sem);
}

void ecrire_position(float x, float y, float addr) {
    char nom_fichier[16];

    // if (addr == XX) addr = xx; // on écrit les coordonnées du beacon XX à la ligne xx 
    // if (addr == YY) addr = yy; // on écrit les coordonnées du beacon YY à la ligne yy
    if (addr == 15) addr = 0; // on écrit les coordonnées du beacon 15 à la ligne 0 
    else return;

    sprintf(nom_fichier, "position_robot%d", (int)addr);
    FILE *fichier = fopen(nom_fichier, "w"); // ouvrir en "r+"?
    CHECK(fichier, NULL, "Erreur lors de l'ouverture du fichier");
    fprintf(fichier, "%.3f %.3f", x, y);
    fclose(fichier);
}

int main () {
    const char * ttyFileName;
    ttyFileName = DEFAULT_TTY_FILENAME;

    // Init
    struct MarvelmindHedge * hedge=createMarvelmindHedge ();
    CHECK(hedge, NULL, "Error: Unable to create MarvelmindHedge");
    hedge->ttyFileName=ttyFileName;
    hedge->verbose=false; // ne pas display "Opened serial port ..."
    hedge->anyInputPacketCallback= semCallback;
    startMarvelmindHedge (hedge);

    // Set Ctrl-C handler
    signal (SIGINT, CtrlHandler);
    signal (SIGQUIT, CtrlHandler);

	sem = sem_open(DATA_INPUT_SEMAPHORE, O_CREAT, 0777, 0);

    // Main loop
    while ((!terminateProgram) && (!hedge->terminationRequired)) {

        // Set timer
        CHECK(clock_gettime(CLOCK_REALTIME, &ts), -1, "clock_gettime error");
		ts.tv_sec += 2;
		sem_timedwait(sem,&ts);

        // Récupérer positions et écrire dans fichier positions
        float *x = (float*)malloc(sizeof(float));
        float *y = (float*)malloc(sizeof(float));
        float *addr = (float*)malloc(sizeof(float));

        getPositionFromMarvelmind(hedge, true, x, y, addr);
        ecrire_position(*x, *y, *addr);

        free(x);
        free(y);    
        free(addr);
    }

    // Exit
    stopMarvelmindHedge (hedge);
    destroyMarvelmindHedge (hedge);
    return 0;
}
