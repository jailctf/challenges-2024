CFLAGS := $(CFLAGS) $(if $(DEBUGLVL),-DDEBUGLVL=$(DEBUGLVL),) $(shell python3.12-config --cflags) -Wall -fPIC -O3
LDFLAGS := $(LDFLAGS) $(shell python3.12-config --ldflags) -shared -fPIC -O3 -fPIE -pie -lpython3.12 #-Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions -lpython3.12

all: embedder

embedder.o: embedder.c

embedder: embedder.o
	$(CC) -o $@ $< $(LDFLAGS)
	strip $@

.PHONY: all clean run single fresh

run: embedder
	$(PWD)/$< $(ARGS)

single: $(FILE)
	$(CC) $< $(CFLAGS) $(LDFLAGS)
	./a.out
	rm -f ./a.out

clean:
	rm -f embedder.o embedder

fresh: clean embedder
