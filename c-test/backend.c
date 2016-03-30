/*
 * @File     backend.c
 * @Author   guojy
 * @Desc     This program displays how to create backend-running applications
 * @Note     exec command line 'gcc backend.c -o backend && ./backend && ps aux | grep backend'
	     in shell,you'll see your backend application ; 
	     Use 'kill -9 {PID}' to terminate your aplication;
 */
#include<unistd.h>
#include<stdlib.h>
#include<stdio.h>

int main(int *argc,char **argv)
{
	if(fork())
	{
		exit(0);
	}
	else
	{
		while(1)
		{
			printf("Doing periodic tasks");
			/** 
			    Define
			    Your
			    Own
			    Task
			    Here
                            !!!
                        **/
			sleep(2);
		}
	}
}

