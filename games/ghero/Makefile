# UNIVERSIDADE FEDERAL DE MINAS GERAIS
# Projeto de monografia
# Arthur Phillip F. Silva
# Professor Pedro O. S. Vaz de Melo

ALLEGRO_VERSION=5.0.10
MINGW_VERSION=4.7.0

FILE_EXE=ghero

FLAGS=-Wall

# Especifididades de sistema
ifeq ($(OS),Windows_NT)
    #Windows stuff
FOLDER=C:
FOLDER_NAME=\allegro-$(ALLEGRO_VERSION)-mingw-$(MINGW_VERSION)
PATH_ALLEGRO=$(FOLDER)$(FOLDER_NAME)
LIB_ALLEGRO=\lib\liballegro-$(ALLEGRO_VERSION)-monolith-mt.a
INCLUDE_ALLEGRO=\include
I=-I

RM=del

else
    #Linux stuff
PATH_ALLEGRO=
LIB_ALLEGRO=-lallegro -lallegro_font -lallegro_ttf
INCLUDE_ALLEGRO=
I=

RM=rm

endif

all: $(FILE_EXE).exe

$(FILE_EXE).exe: $(FILE_EXE).o
	gcc -o $(FILE_EXE).exe $(FILE_EXE).o $(PATH_ALLEGRO)$(LIB_ALLEGRO) $(FLAGS)

$(FILE_EXE).o: $(FILE_EXE).c
		gcc $(I) $(PATH_ALLEGRO)$(INCLUDE_ALLEGRO) -c $(FILE_EXE).c $(FLAGS)

clean:
	$(RM) *.o *.exe *.out
