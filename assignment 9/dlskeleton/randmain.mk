all: randmain randlibhw.so randlibsw.so

randlibhw.so: randlibhw.c
	$(CC) randlibhw.c -shared -fPIC $(CFLAGS) -o $@

randlibsw.so: randlibsw.c
	$(CC) randlibsw.c -shared -fPIC $(CFLAGS) -o $@

randmain: randmain.c randcpuid.c
	$(CC) randmain.c randcpuid.c -ldl -Wl,-rpath=. $(CFLAGS) -o randmain