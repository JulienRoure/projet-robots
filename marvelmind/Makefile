marvelmind_getposition: marvelmind.c tracker.c
	gcc -pthread -c marvelmind.c -o marvelmind.o
	gcc -pthread -c tracker.c -o tracker.o
	gcc -o marvelmind_getposition tracker.o marvelmind.o -pthread

clean:
	rm -f *.o mamarvelmind_getposition
