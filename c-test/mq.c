/*
 * @File     mq.c
 * @Author   guojy
 * @Desc     This program displays usage of message queue
 * @Detail   http://blog.csdn.net/yikai2009/article/details/8645941 
 */

#include<stdio.h>
#include<stdlib.h>
#include<sys/ipc.h>
#include<sys/msg.h>
#include<sys/types.h>
#include<unistd.h>
#include<string.h>

/* @define key_t ftok(const char *pathname,int proj_id);
 * @more http://linux.die.net/man/3/ftok
 */

/* @define int msgsnd(int msqid,struct msgbuf *msgp,int msgsz,int msgflg);
 * @param msgid: identifier of opened message queue
 * @param msgp : pinter pointing to message buffer.
 * @param msgsz: length of message data
 * @param msgflg: that's IPC_NOWAIT,indicating that "msgsnd " action will be blocked
 *               if there's not enough space in message queue for the message to be 
 *               sent;
 */

/* @note: data structure of `struct msgbuf` is as follows:
 * {
 *   long mtype;
 *   char mtxet[1];   
 * }
 * mtype standing for message type
 * mtext indicates the [head] address of message data
 */

/* @define int msgrcv(int msqid,struct msgbuf *msgp,int msgsz,long msgtyp,int msgflg);
 * @desc   The receiver process read a `msgtyp` message out from  mesage queue identified by msqid
 *         into  msgbuf. Once done, this message will be removed from message queue;
 */

/** Here is a demo program **/

#define MSGQ  "/tmp/2"

struct msg_buf
{
	int	mtype;
	char	data[255];
};

int main()
{
	key_t key;
	int msgqid;
	int ret;
	struct msg_buf p_msgbuf;
	struct msg_buf c_msgbuf;
	
	key = ftok(MSGQ,'a');
	printf("key=%d\n",key);  /** output in HEX mode**/
	msgqid = msgget(key,IPC_CREAT|0666);
        printf("msgqid = %d \n",msgqid);	
	if(msgqid == -1)
	{
		printf("Error Creating message queue !!!\n");
		return -1;
	}
	
	if(fork()){
		/**parent process - message sender**/
		p_msgbuf.mtype = getpid();
		strcpy(p_msgbuf.data,"true lover");
		ret = msgsnd(msgqid,&p_msgbuf,sizeof(p_msgbuf.data),IPC_NOWAIT);
		if(ret == -1)
		{
			printf("Error:parent process %d sending message into mq !!\n",getpid());
			exit(1);
		}
		printf("Message sending done.");
		/**wait for child process done**/ 
		
		
	}
	else
	{
		/**child process - message receiver**/
		/**give parent process 5 secends to send message **/
		sleep(5);
		printf("Child process %d starts working",getpid());
		ret = msgrcv(msgqid,&c_msgbuf,sizeof(c_msgbuf.data),getppid(),IPC_NOWAIT);
		if(ret == -1)
		{
			printf("Child process %d error reveiveing message.\n");
			exit(1);
		}
		printf("Received message: %s",c_msgbuf.data);		
		
	}
	
}











