CC = gcc
CFLAGS = -Wall -Wextra -pedantic

# List of object files
OBJ = marvelmind.o tracker.o parser.o main_thread.o

# Main target
thread: main

proc: marvelmind_c parser main_proc

# Compile object files
%.o: %.c
	$(CC) $(CFLAGS) -pthread -c $< -o $@

# Link object files to create the executable
main: $(OBJ)
	$(CC) $(CFLAGS) -pthread $(OBJ) -o getposition




marvelmind_c:
	gcc -g -pthread -c marvelmind.c -o marvelmind.o
	gcc -g -pthread -c tracker.c -o tracker.o
	gcc -o marvelmind_c tracker.o marvelmind.o -pthread

main_proc: main_proc.o
	$(CC) $(CFLAGS) $^ -o $@

main_proc.o: main_proc.c
	$(CC) $(CFLAGS) -c $< -o $@

parser: parser.o
	$(CC) $(CFLAGS) $^ -o $@

parser.o: parser.c
	$(CC) $(CFLAGS) -c $< -o $@




# Clean up object files and executable
clean:
	rm -f $(OBJ) *.o main
