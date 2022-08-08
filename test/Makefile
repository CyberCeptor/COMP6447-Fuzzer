CC = gcc
CFLAGS = -m32

.PHONY: all
all: plaintext csv json

plaintext: plaintext.c

csv: csv.c

json: json.c cJSON.c

.PHONY: clean
clean:
	rm -f *.o plaintext csv json
