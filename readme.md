# allegro_game_ai
# Arthur Phillip Silva

# Conteudo
* Instalando Allegro
 * Linux

# Instalando Allegro
## Linux
* Dependencias Obrigatórias
`sudo apt-get install build-essential subversion cmake xorg-dev libgl1-mesa-dev libglu-dev`
* Módulos
`sudo apt-get install libpng-dev libz-dev libcurl4-gnutls-dev libfreetype6-dev libjpeg-dev libvorbis-dev libopenal-dev libphysfs-dev libgtk2.0-dev libasound-dev libflac-dev libdumb1-dev`
* Documentação
`sudo apt-get install exuberant-ctags dvi2ps dvipdfmx latex2html pandoc`
* Código-fonte
`svn co https://alleg.svn.sourceforge.net/svnroot/alleg/allegro/branches/5.0 allegro-5.0`
`cd allegro-5.0`
ou
`git clone https://github.com/liballeg/allegro5.git`
`cd allegro`
`git checkout 5.0`
* Preparar instalação
`mkdir build
 cd build`
`cmake -DCMAKE_INSTALL_PREFIX=/usr ..`
* Instalar
`make
 sudo make install`
---
Para usar deve incluir no arquivo.c
`#include <allegro5/allegro.h>`
e compilar com
`gcc -lallegro arquivo.c`

Refs:
[Rafael Toledo](http://www.rafaeltoledo.net/compilando-e-instalando-a-biblioteca-allegro-5-no-ubuntu/)
[Wiki Allegro](https://wiki.allegro.cc/index.php?title=Install_Allegro5_From_Git/Linux/Debian)

## Windows
* Faça o [download](https://github.com/liballeg/allegro5/releases/download/5.0.11/allegro-5.0.11.zip) do Allegro.
* Extraia o conteúdo para a pasta C:.
* Faça o [download](https://sourceforge.net/projects/mingw/files/latest/download?source=files) do MinGW.
* Instale o MinGW.
---
Para usar deve incluir no arquivo.c
`#include <allegro5/allegro.h>`,
cpopiar o arquivo _allegro-5.0.11-monolith-mt.dll_ para a pasta do prejeto
e compilar com
`gcc -I C:\allegro-5.0.11-mingw-4.7.0\include -c arquivo.c -o arquivo.o
 gcc -o arquivo.exe arquivo.o C:\allegro-5.0.11-mingw-4.7.0\lib\liballegro-5.0.11-monolith-mt.a`
