# [allegro_game_ai](readme)
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
`#include <allegro5/allegro.h>` </br>
e compilar com </br>
`gcc -lallegro arquivo.c`

Refs:
[Rafael Toledo](http://www.rafaeltoledo.net/compilando-e-instalando-a-biblioteca-allegro-5-no-ubuntu/),
[Wiki Allegro](https://wiki.allegro.cc/index.php?title=Install_Allegro5_From_Git/Linux/Debian)

## Windows
* CMAKE (Opcional)
  * Faça o [download](https://cmake.org/download/) e instale o CMake.
* MINGW
  * Faça o [download](https://sourceforge.net/projects/mingw/files/latest/download?source=files) do MinGW.
  * Instale o MinGW.
    * Instale as dependencias na pasta _C:_ .
    * mingw32-autoconf
    * mingw32-automake
    * mingw32-binutils
    * mingw32-bzip2
    * mingw32-dos2unix
    * mingw32-gcc
    * mingw32-gcc-g++
    * mingw32-gdb
    * mingw32-libgcc
    * mingw32-make
  * Inclua a path do MinGW no sistema. <\br>
   Para isso entre em Meu Computador>Propriedades>Configurações Avanaçadas do Sistema>Variáveis de Sistema e inclua "C:\MinGW\bin" em PATH 
  * para facilitar o uso do make <\br> 
  `copy c:\MinGW\bin\mingw32-make.exe c:\MinGW\bin\make.exe`
* ALLEGRO
  * Faça o [download](http://cdn.allegro.cc/file/library/allegro/5.0.10/allegro-5.0.10-mingw-4.7.0.zip) do Allegro 5.0.10.
  * Extraia o conteúdo para a pasta _C:_ .

 ---
Para usar deve incluir no _arquivo.c_ </br>
`#include <allegro5/allegro.h>`, </br>
copiar o arquivo _C:\allegro-5.0.10-mingw-4.7.0\bin\allegro-5.0.11-monolith-mt.dll_ para a pasta do projeto </br>
e compilar com </br>
`gcc -I C:\allegro-5.0.10-mingw-4.7.0\include -c arquivo.c -o arquivo.o` </br>
`gcc -o arquivo.exe arquivo.o C:\allegro-5.0.10-mingw-4.7.0\lib\liballegro-5.0.10-monolith-mt.a` </br>

Refs:
[Pedro Olmo](https://www.youtube.com/watch?v=AezxBP687n8&t=9s), 
[Ezequiel França](https://github.com/ezefranca/Master-Exploder/wiki/Compila%C3%A7%C3%A3o-e-Instala%C3%A7%C3%A3o-Allegro-5-e-OpenCV-no-Windows)
Recomenda-se o uso de makefile

---
Para este projeto foram utilizados o Allegro 5.0.10 com MinGW 4.7.0 .
