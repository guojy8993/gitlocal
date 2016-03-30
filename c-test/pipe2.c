/*
 *@file pipe.c
 *@note This program displays usage of `pipe` communication
 */

#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>

int pipe_default[2];

int main(){
    pid_t pid;
    printf("Length of type `pid_t`: %d\n",sizeof(pid_t));

    char buff[32];
    printf("Length of `char` type: %d\n",sizeof(char));
    memset(buff,0,32);
    /** create pipe**/
    if(pipe(pipe_default)<0){
        printf("fail to create pipe.");
	return 0;
    }
    /** create child process**/
    if((pid = fork()) == 0){
    	/** child **/
	printf("This is child process %d with parent %d .\n",getpid(),getppid());
        sleep(3);
	/** block the write end **/        
	close(pipe_default[1]);
        if(read(pipe_default[0],buff,32) > 0){
		printf("Received data from parent: %s.\n",buff);
		
	}
	close(pipe_default[0]);

    }else{
	/** prent process code **/
	printf("This is parent process with pid %d.\n",getpid());	
	close(pipe_default[0]);
	write(pipe_default[1],"hello",strlen("hello"));
	close(pipe_default[1]);
	printf("Waiting child process to exit ... \n");
	waitpid(pid,NULL,0);
    }
   
}
