/* 
 * @file alarm.c
 * @note This program displays usage of `SIFALRM`
 */
#include<signal.h>
#include<stdio.h>

void handler(int sig){
    printf("Received SIGALRM signal and signum is %d\n",SIGALRM);
}

int main(){
    signal(SIGALRM,handler);
    alarm(5);
    int i=0;
    for(;i<7;i++)
    {
       printf("Second %d\n",i);
       sleep(1);
    }    
    return 0;
}
