CC = gcc
CFLAGS = -m32 -fno-stack-protector -z execstack -no-pie -Wno-implicit-function-declaration

all: spelunk

spelunk: spelunk.c
	$(CC) $(CFLAGS) -o spelunk spelunk.c

clean:
	rm -f spelunk
