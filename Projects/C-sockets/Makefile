CC=gcc
binaries=client

all: clean $(binaries)
client: client.c
	$(CC) client.c -o client -Wall -g -lssl
clean:
	rm -f *.o client
