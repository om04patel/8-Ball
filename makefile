# Compiler and compiler flag variables
CC := clang
CFLAGS := -Wall -pedantic -std=c99 -fPIC
PYTHON_INCLUDE := /usr/include/python3.11/
LIBS := -lm
PYTHON_LIB := /usr/lib/python3.11
SWIG := swig

# Default target
all: _phylib.so

# Target for phylib.o
phylib.o: phylib.c
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

# Target for libphylib.so
libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o $(LIBS)

# Targets for SWIG generated files (phylib_wrap.c and phylib.py)
phylib_wrap.c phylib.py: phylib.i
	$(SWIG) -python phylib.i

# Target for phylib_wrap.o
phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -I$(PYTHON_INCLUDE) -c phylib_wrap.c -o phylib_wrap.o

# Target for _phylib.so
_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L$(PYTHON_LIB) -lpython3.11 -lphylib -o _phylib.so

# Clean target
clean:
	rm -f *.o *.so phylib_wrap.c phylib.py
