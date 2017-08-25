# allegro_game_ai
## Arthur Phillip Silva

# Conteudo
* [Instalando Allegro](#instalando-allegro)
 * [Linux](#linux)
 * [Windows](#windows)

# Instalando Allegro
## Linux

* Dependencias Obrigatórias </br>
`sudo apt-get install build-essential subversion cmake xorg-dev libgl1-mesa-dev libglu-dev`

* Módulos </br>
`sudo apt-get install libpng-dev libz-dev libcurl4-gnutls-dev libfreetype6-dev libjpeg-dev libvorbis-dev libopenal-dev libphysfs-dev libgtk2.0-dev libasound-dev libflac-dev libdumb1-dev`

* Documentação </br>
`sudo apt-get install exuberant-ctags dvi2ps dvipdfmx latex2html pandoc`

* Código-fonte </br>
`svn co https://alleg.svn.sourceforge.net/svnroot/alleg/allegro/branches/5.0 allegro-5.0` </br>
`cd allegro-5.0` </br>
ou </br>
`git clone https://github.com/liballeg/allegro5.git` </br>
`cd allegro` </br>
`git checkout 5.0` </br>
* Preparar instalação </br>
`mkdir build` </br>
`cd build` </br>
`cmake -DCMAKE_INSTALL_PREFIX=/usr ..` </br>
* Instalar </br>
`make` </br>
`sudo make install`
---
Para usar deve incluir no arquivo.c </br>
`#include <allegro5/allegro.h>`
e compilar com </br>
`gcc -lallegro arquivo.c`

Refs:
[Rafael Toledo](http://www.rafaeltoledo.net/compilando-e-instalando-a-biblioteca-allegro-5-no-ubuntu/),
[Wiki Allegro](https://wiki.allegro.cc/index.php?title=Install_Allegro5_From_Git/Linux/Debian)

## Windows
* Faça o [download](https://github.com/liballeg/allegro5/releases/download/5.0.11/allegro-5.0.11.zip) do Allegro.
* Extraia o conteúdo para a pasta C:.
* Faça o [download](https://sourceforge.net/projects/mingw/files/latest/download?source=files) do MinGW.
* Instale o MinGW.
---
Para usar deve incluir no arquivo.c </br>
`#include <allegro5/allegro.h>`, </br>
copiar o arquivo _allegro-5.0.11-monolith-mt.dll_ para a pasta do prejeto </br>
e compilar com </br>
`gcc -I C:\allegro-5.0.11-mingw-4.7.0\include -c arquivo.c -o arquivo.o` </br>
`gcc -o arquivo.exe arquivo.o C:\allegro-5.0.11-mingw-4.7.0\lib\liballegro-5.0.11-monolith-mt.a`
