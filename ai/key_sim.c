#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/input.h>
#include <sys/time.h>
#include <stdint.h>

#define KEYBOARD_DEVICE_PATH  "/dev/input/event3"

int simularTecla( uint16_t tecla )
{
    int fd = -1;
    struct input_event k;

    /* Obtem um descritor para o dispositivo (teclado) */
    fd = open( KEYBOARD_DEVICE_PATH, O_WRONLY | O_NONBLOCK );

    if( fd < 0 )
	{
		printf("Erro fd\n");
		return -1;
	}

    /* Toma controle exclusivo do teclado */
    if(ioctl( fd, EVIOCGRAB, 1 ))
        return -1;

    /* Pressionando Tecla */
    // k.type = EV_KEY;
    // k.value = 1;
    // k.code = tecla;
    // gettimeofday( &k.time, NULL );
    // write( fd, &k, sizeof(struct input_event) );

    k.type = EV_KEY;
    k.value = 1;
    k.code = tecla;
    gettimeofday( &k.time, NULL );
    write( fd, &k, sizeof(struct input_event) );

    /* Soltando Tecla */
    k.type = EV_KEY;
    k.value = 0;
    k.code = tecla;
    gettimeofday( &k.time, NULL );
    write( fd, &k, sizeof(struct input_event) );

    /* Liberando controle do teclado */
    ioctl( fd, EVIOCGRAB, 0 );

    /* Fechando descritor para o dispositivo (teclado) */
    close(fd);

    /* Sucesso*/
    return 0;
}


int main( void )
{
    /* Sequencia de teclas */
    // uint16_t teclas[] = { KEY_L, KEY_S, KEY_SPACE, KEY_MINUS, KEY_A, KEY_L, KEY_ENTER };
    uint16_t teclas[] = { KEY_A, KEY_T, KEY_O, KEY_M, KEY_ENTER };
    unsigned int count =  sizeof(teclas) / sizeof(teclas[0]);
    unsigned int i = 0;

    /* Simula sequencia de teclas */
    for( i = 0; i < count; i++ )
	{
		printf("tent %d", teclas[i]);
		printf(" %d\n",simularTecla( teclas[i]) );
	}

    return 0;
}
