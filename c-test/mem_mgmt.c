#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main(){
	char name[100];
	char *desc;
	
	strcpy(name,"Guojingyu");
	desc = malloc(200*sizeof(char));
	if(desc == NULL){
		fprintf(stderr,"Unable to malloc more memory.");
	}else{
		strcpy(desc,"abcdefghijklmb");
	}
	
	printf("Name=%s\n",name);
	printf("Description=%s\n",desc);
	
	desc = realloc(desc,100*sizeof(char));
	printf("Desc = %s",desc);

	free(desc);

}
