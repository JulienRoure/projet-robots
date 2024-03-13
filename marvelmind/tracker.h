#ifndef TRACKER_H
#define TRACKER_H

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#if defined(WIN32) || defined(_WIN64)
#include <windows.h>
#else
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <semaphore.h>
#include <time.h>
#endif

#include "marvelmind.h"

extern bool terminateProgram;

#if defined(WIN32) || defined(_WIN64)
BOOL CtrlHandler(DWORD fdwCtrlType);
#else
void CtrlHandler(int signum);
#endif

#if defined(WIN32) || defined(_WIN64)
void sleep(unsigned int seconds);
#endif

#if defined(WIN32) || defined(_WIN64)
void semCallback();
#else
void semCallback();
#endif

#ifdef _WIN64
const wchar_t* GetWC(const char* c);
#endif

int trackerFunction(void);

#endif /* TRACKER_H */
