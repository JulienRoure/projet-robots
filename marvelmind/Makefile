all: marvelmind_tracker

marvelmind_tracker: marvelmind.c tracker.c
	gcc -pthread -c marvelmind.c -o marvelmind.o
	gcc -pthread -c tracker.c -o tracker.o
	gcc -o marvelmind_tracker tracker.o marvelmind.o -pthread
	rm -f *.o

clean:
	rm -f *.o marvelmind_tracker
