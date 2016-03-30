/*
 * @file timer.c
 * @note This program displays usgae of `time.h` 
 * @more http://blog.csdn.net/hbuxiaofei/article/details/35569229
 */

#include<stdio.h>
#include<time.h>
#include<sys/time.h>
#include<stdlib.h>
#include<signal.h>

static int count = 10;

void set_timer(){
    struct itimerval itv;
    itv.it_interval.tv_sec = 1;      /** periodic_interval in seconds **/ 
    itv.it_interval.tv_usec = 0;     /** periodic_interval in microseconds **/

    itv.it_value.tv_sec = 1;         /** fuze_delay in seconds **/
    itv.it_value.tv_usec = 0;        /** fuze_delay in microseconds **/
    setitimer(ITIMER_REAL,&itv,NULL);
}

void signal_handler()
{
    count ++;
    printf("%d\n",count);
}

int main(){
    /** register signal handler for `SIGALRM` **/
    signal(SIGALRM,signal_handler);

    /** starting a timer that sends `SIGALRM` signal with 
        1/periodic_interval frequency after fuze_delay 
        secs **/
    set_timer(); 
    while(count<20);
    exit(0);
    return 1;	
}
