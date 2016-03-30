#include<stdio.h>
#include<errno.h>
#include<string.h>


extern int errno ;

int main(){
	FILE *pf;
	int errnum;
	printf("Error Default Value :%d\n",errno);
	printf("Errornum Default Value :%d\n",errnum);
	
	//pf = fopen("/root/hello.txt","rb");
	pf = fopen("unexist.txt","rb");
	if(pf == NULL){
		printf("Errno after error occurs: %d\n",errno);
		errnum = errno;
		fprintf(stderr,"Value of error:%d\n",errnum);
	}else{
		fclose(pf);
	}
	return 0;
}
