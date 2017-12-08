#define WINVER 0x0500
#include <windows.h>
#include <stdlib.h>
#include <stdio.h>

int press_key(char key, int msec)
{
    INPUT ip; 

    ip.type = INPUT_KEYBOARD;   
    ip.ki.wScan = 0;            
    ip.ki.time = 0;
    ip.ki.dwExtraInfo = 0;
   
    ip.ki.wVk = key;
    ip.ki.dwFlags = 0; 
    SendInput(1, &ip, sizeof(INPUT));
   
    Sleep(msec);
  
    ip.ki.dwFlags = KEYEVENTF_KEYUP; 
    SendInput(1, &ip, sizeof(INPUT));

    return 0;
}

int main()
{
    int      pid = 0;
    char    *jogo = "..\\games\\frogger\\frogger.exe";

    // pid = fork();
    // if(pid == -1)
    // {
	// 	perror("fork");
    //     exit(0);
    // }

    // if (pid == 0)
    // {   // Processo Filho

    //     // E transformado em um novo Processo
    //     // Em caso de erro o processo e terminado
    //     if (execl(jogo) < 0)
    //     {
    //         fprintf(stderr, "Programa '%s' nao encontrado\n",
    //         jogo);
    //     }
    //     exit(0);
    // }
    // else
    // {
    //     // Processo Pai
    //     // Espera que o filho termine
    //     do {
    //         p[1] = waitpid(p[0], &r, WUNTRACED);
    //     } while (!WIFEXITED(r) && !WIFSIGNALED(r));
    // }

    // execl("C::\\WINDOWS\\SYSTEM32\\CMD.EXE", "cmd.exe", "/c", "echo", "foo", ">C::\\Users\\foo.txt"); 
    system("..\\games\\frogger\\frogger.exe"); 
    
    press_key('W', 10);
    press_key('W', 100);
    press_key('D', 100);
    press_key('D', 10);
    press_key('W', 200);
   
    // char a = 0x41;
    // printf("%c \n", a);
 
    // Exit normally
    return 0;
}