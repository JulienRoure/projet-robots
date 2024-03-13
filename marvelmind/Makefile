CC = gcc
CFLAGS = -Wall -Wextra -pthread

# List of object files
OBJ = marvelmind.o tracker.o parser.o main_thread.o

# Main target
all: main

# Compile object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Link object files to create the executable
main: $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o getposition

# Clean up object files and executable
clean:
	rm -f $(OBJ) main
