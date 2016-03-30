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

    /** The memset() function fills the first n bytes of the
        memory area pointed to by s with the constant byte c. 
        @note #include<string.h>
        void *memset(void *s,int c,size_t n)  **/
    memset(buff,0,32);
    /** create pipe with 2-int-element array
        if successful , arr[0] stands for the `read` file-descriptor;
        and arr[1] stands for the `write` file-descriptor;  
        @note #include<unistd.h>
        int pipe(int fd[2]); **/ 
    if(pipe(pipe_default) < 0)
    {
    	printf("Failed to create pipe !\n");
        return 0;
    }
    /** Once fork() executed, two process spawned: parent-process with 
        pid > 0 and child-process with pid=0 . A negtive value of pid 
        usually predicts a failure of forking 
        @note include<unistd.h>
        pid_t fork(void); **/
    if((pid = fork()) == 0){

        printf("I'm child process,my pid is %d ,and my parent is %s",getpid(),getppid());
        /** **/

    	close(pipe_default[1]);
        sleep(5);
        if(read(pipe_default[0],buff,32) > 0)
        {
		printf("Received data from parent: %s \n",buff);
        }
        close(pipe_default[0]);
        printf("Child Process exited.");
    }else{
     
        printf("I'm parent process,my pid is %d ,and my parent is %s",getpid(),getppid());

        /** The child-reading side of the pipe needs to be blocked
	    while parent trying to write something into pipe in case of
            simultaneous operation on pipe **/

 	close(pipe_default[0]);
        if(write(pipe_default[1],"hello",strlen("hello")) !=-1)
        {
        	printf("Sends data to child,hello! \n");
        }
        close(pipe_default[1]);

        /** wait child interrupted or exited**/
        waitpid(pid,NULL,0);
        printf("Parent processs exited.");
    }    
}
