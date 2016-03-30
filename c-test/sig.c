/*
 * This program displays usage of `signal.h`
 * Read `http://blog.csdn.net/yikai2009/article/details/8643818` for more.
 * 
 *
 */

#include<stdio.h>
#include<stdlib.h>
#include<signal.h>

int value = 0;
void func(int sig)
{
    switch(sig)
    {
      case SIGINT:  printf(" i get a `sigint` signal !! \n");break;
      case SIGKILL: printf(" i get a `sigkill` signal !! \n");break;
      case SIGSTOP: printf(" i get a `sigstop` signal !! \n");break;
      case SIGQUIT: printf(" i get a `sigquit` signal !! \n");break;
      case SIGTERM: printf(" i get a `sigterm` signal !! \n");break;
      case SIGCHLD: printf(" i get a `sigchld` signal !! \n");break;
      case SIGALRM: printf(" i get a `sigalrm` signal !! \n");break;
      default:      printf(" i get a signal and signum is %d!! \n",sig);
    }
    value = 1;
}

int main()
{
    int i=0;   

    /** SIGINT  2**/
    // printf("SIGINT is %d \n",SIGINT);
    signal(SIGINT,func);

    /** SIGQUIT **/
    // printf("SIGQUIT is %d \n",SIGQUIT);
    signal(SIGQUIT,func);

    /** SIGSTOP**/
    // printf("SIGSTOP is %d \n",SIGSTOP);
    signal(SIGSTOP,func);

    /** SIGCHLD**/
    // printf("SIGCHLD is %d \n",SIGCHLD);
    signal(SIGCHLD,func);

    /** SIGTERM**/
    // printf("SIGTERM is %d \n",SIGTERM);
    signal(SIGTERM,func);

    /** SIGKILL**/
    // printf("SIGKILL is %d \n",SIGKILL);
    signal(SIGKILL,func);

    while(!value){
   	sleep(1);
    }
    
    /** SIGALRM**/
    signal(SIGALRM,func);
    alarm(5);
    
    for(;i<10;i++)
    {
       printf("Second %d\n",i);
       sleep(1);
    }

    return 0;
}
