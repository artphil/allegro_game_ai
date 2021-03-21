ALLEGRO_VERSION=5.0.10
PATH_ALLEGRO=C:\allegro-$(ALLEGRO_VERSION)-mingw-4.7.0
LIB_ALLEGRO=\lib\liballegro-$(ALLEGRO_VERSION)-monolith-mt.a
INCLUDE_ALLEGRO=\include

all: ghero.exe 

ghero.exe: ghero.o 
	gcc -o ghero.exe ghero.o $(PATH_ALLEGRO)$(LIB_ALLEGRO)	
	
ghero.o: ghero.c 
	gcc -I $(PATH_ALLEGRO)$(INCLUDE_ALLEGRO) -c ghero.c

clean:
	del ghero.o 
	del ghero.exe