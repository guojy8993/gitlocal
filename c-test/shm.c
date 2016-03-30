/* @File   shm.c
 * @Desc   This program displays usage of sharing
 *          memory among processes;
 * @Author guojy
 * @Date   2015/12/25
 */
#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<errno.h>
#include<unistd.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<sys/ipc.h>
#include<sys/shm.h>

/*
 *@note S_IRUSR: Permits the file's owner to read it
 *@note S_IWUSR: Permits the file's owner to write to it
 *@note S_IRGRP:  Permits the file's group to read it
 *@note S_IWGRP:  Permits the file's group to write to it
 */
/*
 *@note RW by User
 */
#define PERM S_IRUSR|S_IWUSR

int main(int argc,char **argv)
{
	int shmid;
	char *p_addr,*c_addr;
	
	if(argc!=2)
	{
		fprintf(stderr,"Usage:%s\n\a",argv[0]);
		exit(1);
	}
	
	/** @note    create shared memory
            @define  int shmget(key_t key,size_t size,int shmflg);
	    @more    "http://linux.die.net/man/3/shmget" **/
        if((shmid=shmget(IPC_PRIVATE,1024,PERM))==-1)
	{
		fprintf(stderr,"Failed to Create shared memory:%s\n\a",strerror(errno));
		exit(1);
	}
	/** create parent process and child process**/
	if(fork())
	{
		/** @define void *shmat(int shmid,const void *shmaddr,int shmflg);
                    @desc   This function attaches the shared memory segment associated with 
                            the shared memory identifier specified by shmid to the address 
                            space of the calling process
                    @more http://linux.die.net/man/3/shmat **/
		
		p_addr=shmat(shmid,0,0);
		memset(p_addr,'\0',1024);

		/** @define char *strncpy(char *dest,const char *src,size_t n);
		    @define char *strcpy(char *dest,const char *src); 
		    @more   http://linux.die.net/man/3/strncpy **/
		strncpy(p_addr,argv[1],1024);
		
		/** @desc wait child process to stop or terminated
		    @define pid_t wait(int *stat_loc);
		    @define pid_t waitpid(pid_t pid, int *stat_loc,int options);  
		    @more   http://linux.die.net/man/3/wait**/
		wait(NULL);  // 释放资源不关心终止状态
		exit(0);
	}
	else
	{
		sleep(1);
		c_addr=shmat(shmid,0,0);
		printf("Client get %s \n",c_addr);
		exit(0);
	}	

}
