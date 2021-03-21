#include <stdio.h>
#include <math.h>
#include <allegro5/allegro.h>
#include <allegro5/allegro_primitives.h>

#define FPS 30.0
#define SCREEN_W 640
#define SCREEN_H 480
#define BALL_SIZE 25
#define BAR_W 15
#define BAR_H SCREEN_H / 3

void print_reward(ALLEGRO_FILE *fd, int reward)
{
	char txt[6];
	sprintf(txt, "%4d\n", reward);
	al_fflush(fd);
	al_fwrite(fd, txt, sizeof(txt));
}

int main(int argc, char **argv)
{

	ALLEGRO_DISPLAY *display = NULL;
	ALLEGRO_EVENT_QUEUE *event_queue = NULL;
	ALLEGRO_TIMER *timer = NULL;
	ALLEGRO_BITMAP *ball = NULL;
	ALLEGRO_BITMAP *bar = NULL;
	ALLEGRO_BITMAP *bar2 = NULL;
	bool redraw = true;

	ALLEGRO_FILE *text_out = al_fopen_fd(1, "w");
	int score = 0;

	// ------------------------ modificando os valores de entrada ----------------------------------

	int x, playing = 1;
	int count1 = 0, count2 = 0;
	float veloc = 0.0;
	int collide1, collide2;

	//posicoes x e y iniciais de ball
	float ball_x = SCREEN_W / 2.0 - BALL_SIZE / 2.0;
	float ball_y = SCREEN_H / 2.0 - BALL_SIZE / 2.0;
	//o quanto as posicoes x e y vao variar ao longo do tempo. No t=1, se x de ball eh 40, no t=2, x do ball eh 40 + ball_dx = 36
	float ball_dx = -5.0, ball_dy = 10.0;

	//posicoes x e y iniciais de barra 1
	float bar_x = 10.0;
	float bar_y = SCREEN_H / 2.0 - BAR_H / 2.0;
	float bar_dy = 30.0;

	//posicoes x e y iniciais de barra 2
	float bar2_x = SCREEN_W - BAR_W - 10.0;
	float bar2_y = SCREEN_H / 2.0 - BAR_H / 2.0;
	float bar2_dy = 9.0;

	//------------------------------ procedimentos de inicializacao ----------------------------
	if (!al_init())
	{
		fprintf(stderr, "failed to initialize allegro!\n");
		return -1;
	}

	timer = al_create_timer(1.0 / FPS);
	if (!timer)
	{
		fprintf(stderr, "failed to create timer!\n");
		return -1;
	}

	display = al_create_display(SCREEN_W, SCREEN_H);
	if (!display)
	{
		fprintf(stderr, "failed to create display!\n");
		al_destroy_timer(timer);
		return -1;
	}

	event_queue = al_create_event_queue();
	if (!event_queue)
	{
		fprintf(stderr, "failed to create event_queue!\n");
		al_destroy_timer(timer);
		al_destroy_display(display);
		return -1;
	}

	al_install_keyboard();
	al_init_primitives_addon();
	al_start_timer(timer);

	// ----------------- cria a fila de eventos ----------------------------------------

	//registra que a fila de eventos deve detectar quando uma tecla for pressionada no teclado
	al_register_event_source(event_queue, al_get_keyboard_event_source());

	//registra na fila de eventos que eu quero identificar quando a tela foi alterada
	al_register_event_source(event_queue, al_get_display_event_source(display));

	//registra na fila de eventos que eu quero identificar quando o tempo alterou de t para t+1
	al_register_event_source(event_queue, al_get_timer_event_source(timer));

	// ALLEGRO_KEYBOARD_STATE keyState;

	//-----------------------------------------------------------------------------------------

	playing = 1;
	collide1 = 0;
	collide2 = 0;
	veloc = 0.0;
	count1 = 0;
	count2 = 0;
	ball_x = SCREEN_W / 2.0 - BALL_SIZE / 2.0;
	ball_y = SCREEN_H / 2.0 - BALL_SIZE / 2.0;
	ball_dx = -5.0;

	//cria um bitmap quadrangular de tamanho BALL_SIZE
	ball = al_create_bitmap(BALL_SIZE, BALL_SIZE);
	if (!ball)
	{
		fprintf(stderr, "failed to create ball bitmap!\n");
		al_destroy_display(display);
		al_destroy_timer(timer);
		return -1;
	}

	// cria barra 1
	bar = al_create_bitmap(BAR_W, BAR_H);
	if (!bar)
	{
		fprintf(stderr, "failed to create bar bitmap!\n");
		al_destroy_display(display);
		al_destroy_timer(timer);
		al_destroy_bitmap(ball);
		return -1;
	}

	// cria barra 2
	bar2 = al_create_bitmap(BAR_W, BAR_H);
	if (!bar2)
	{
		fprintf(stderr, "failed to create bar bitmap!\n");
		al_destroy_display(display);
		al_destroy_timer(timer);
		al_destroy_bitmap(ball);
		al_destroy_bitmap(bar);
		return -1;
	}

	//avisa o allegro que eu quero modificar as propriedades do ball
	al_set_target_bitmap(ball);
	//altera a cor do ball para rgb(255,0,255)
	al_clear_to_color(al_map_rgb(255, 255, 255));
	//avisa o allegro que agora eu quero modificar as propriedades da tela
	al_set_target_bitmap(al_get_backbuffer(display));
	//colore a tela de preto (rgb(0,0,0))
	al_clear_to_color(al_map_rgb(0, 0, 0));

	// parametros da barra 1
	al_set_target_bitmap(bar);
	al_clear_to_color(al_map_rgb(0, 255, 0));
	al_set_target_bitmap(al_get_backbuffer(display));
	al_clear_to_color(al_map_rgb(0, 0, 0));

	// parametros da barra 2
	al_set_target_bitmap(bar2);
	al_clear_to_color(al_map_rgb(255, 0, 0));
	al_set_target_bitmap(al_get_backbuffer(display));
	al_clear_to_color(al_map_rgb(0, 0, 0));

	print_reward(text_out, score);

	//loop infinito, ou seja, enquanto playing for verdadeiro, faca:
	while (playing == 1)
	{
		print_reward(text_out, score);

		ALLEGRO_EVENT ev;
		//espera por um evento e o armazena na variavel de evento ev
		al_wait_for_event(event_queue, &ev);

		//se o tipo de evento for um evento do temporizador, ou seja, se o tempo passou de t para t+1
		if (ev.type == ALLEGRO_EVENT_TIMER)
		{
			//verifica se a posicao x do ball passou dos limites da tela
			if (ball_x < 0)
			{
				playing = 0;
				// score -= 11;
				print_reward(text_out, score);
				continue;
			}
			if (ball_x > SCREEN_W - BALL_SIZE)
			{
				playing = 0;
				// score += 11;
				print_reward(text_out, score);
				continue;
			}

			//verifica se a posicao y do ball passou dos limites da tela
			if (ball_y < 0 || ball_y > SCREEN_H - BALL_SIZE)
			{
				//altera a direcao na qual o ball se move no eixo y
				ball_dy = -ball_dy;
			}

			// Ball bate na barra 1
			if ((ball_y + BALL_SIZE > bar_y && ball_y < bar_y + BAR_H) && ball_x < bar_x + BAR_W)
			{
				if (!collide1)
				{
					collide1 = 1;

					ball_dx = fabs(ball_dx);
					count1++;
					score += 10;

					// if (((ball_y + BALL_SIZE) > bar_y && (ball_y + BALL_SIZE / 2.0) < (bar_y + BAR_H / 5.0)) || ((ball_y + BALL_SIZE / 2.0) > (bar_y + 4.0 * BAR_H / 5.0) && (ball_y) < (bar_y + BAR_H)))
					// 	if (ball_dx > 6.0)
					// 		ball_dx -= 1.33;
					// if ((ball_y + BALL_SIZE / 2.0) > (bar_y + 2.0 * BAR_H / 5.0) && (ball_y + BALL_SIZE / 2.0) < (bar_y + 3.0 * BAR_H / 5.0))
					// 	if (ball_dx < 29.0)
					// 		ball_dx += 4.95;
				}
			}
			else
				collide1 = 0;

			// Ball bate na barra 2
			if ((ball_y + BALL_SIZE > bar2_y && ball_y < bar2_y + BAR_H) && ball_x + BALL_SIZE > bar2_x)
			{
				if (!collide2)
				{
					collide2 = 1;

					ball_dx = -fabs(ball_dx);
					count2++;

					// if (((ball_y + BALL_SIZE) > bar2_y && (ball_y + BALL_SIZE / 2.0) < (bar2_y + BAR_H / 5.0)) || ((ball_y + BALL_SIZE / 2.0) > (bar2_y + 4.0 * BAR_H / 5.0) && (ball_y) < (bar2_y + BAR_H)))
					// 	if (ball_dx > 6.0)
					// 		ball_dx += 1.33;
					// if ((ball_y + BALL_SIZE / 2.0) > (bar2_y + 2.0 * BAR_H / 5.0) && (ball_y + BALL_SIZE / 2.0) < (bar2_y + 3.0 * BAR_H / 5.0))
					// 	if (ball_dx < 29.0)
					// 		ball_dx -= 4.95;
				}
			}
			else
				collide2 = 0;

			if (veloc < fabs(ball_dx))
				veloc = fabs(ball_dx);

			//Modificar as propriedades do ball
			x = 255 * (fabs(ball_dx) - 4) / 30;
			al_set_target_bitmap(ball);
			al_clear_to_color(al_map_rgb(x, 100, (255 - x)));
			al_set_target_bitmap(al_get_backbuffer(display));
			al_clear_to_color(al_map_rgb(0, 0, 0));

			// bar2 move sozinha
			// if ((bar2_y + BAR_H / 4.0) > (ball_y + BALL_SIZE / 2.0))
			if ((bar2_y) > (ball_y + BALL_SIZE / 2.0))
			{
				if (bar2_y > 0)
					bar2_y += -bar2_dy;
			}
			if ((bar2_y + BAR_H) < (ball_y + BALL_SIZE / 2.0))
			{
				if (bar2_y < SCREEN_H - BAR_H)
					bar2_y += bar2_dy;
			}

			//faz o ball se mover no eixo x e y incrementando as suas posicoes de ball_dx e ball_dy, respectivamente
			ball_x += ball_dx;
			ball_y += ball_dy;
			redraw = true;
		}

		//se o tipo do evento for uma tecla pressionada
		if (ev.type == ALLEGRO_EVENT_KEY_DOWN)
		{
			//verifica qual tecla foi
			switch (ev.keyboard.keycode)
			{
			//se a tecla for o W
			case ALLEGRO_KEY_W:
				if (bar_y > 0)
					bar_y -= bar_dy;
				score -= 1;
				break;
			//se a tecla for o S
			case ALLEGRO_KEY_S:
				if (bar_y < SCREEN_H - BAR_H)
					bar_y += bar_dy;
				score -= 1;
				break;

			case ALLEGRO_KEY_ESCAPE:
				playing = 0;
				break;
			}
		}

		//se o tipo de evento for o fechamento da tela (clique no x da janela)
		if (ev.type == ALLEGRO_EVENT_DISPLAY_CLOSE)
		{
			playing = 0;
		}

		//se eu alterei a posicao do ball, o redraw foi para true e eu nao tenho eventos na fila para ler
		if (redraw && al_is_event_queue_empty(event_queue))
		{

			redraw = false;
			//limpo a tela
			al_clear_to_color(al_map_rgb(0, 0, 0));
			//desenho o ball nas novas posicoes x e y
			al_draw_bitmap(ball, ball_x, ball_y, 0);
			//desenho o bar nas novas posicoes x e y
			al_draw_bitmap(bar, bar_x, bar_y, 0);
			//desenho o bar2 nas novas posicoes x e y
			al_draw_bitmap(bar2, bar2_x, bar2_y, 0);
			//reinicializo a tela
			al_flip_display();
		}
	} //fim do while

	// -------------------- terminando o jogo ------------------------------------------
	print_reward(text_out, score);
	print_reward(text_out, score);
	al_rest(0.2);

	al_destroy_timer(timer);
	al_destroy_display(display);
	al_destroy_event_queue(event_queue);

	return 0;
}
