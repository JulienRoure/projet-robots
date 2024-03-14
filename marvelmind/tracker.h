#ifndef TRACKER_H
#define TRACKER_H

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <semaphore.h>
#include <time.h>
#include "marvelmind.h"

extern bool terminateProgram;

void CtrlHandler(int signum);

void semCallback();

int tracker(void);

#endif /* TRACKER_H */
