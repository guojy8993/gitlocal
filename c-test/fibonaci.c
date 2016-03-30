#include<stdio.h>

int fibnaci(int i){
	if(i == 0){
		return 0;
	}
	if(i == 1){
		return 1;
	}
	return fibnaci(i-1)+fibnaci(i-2);
}

int main(){
	int n = 20;
	int i=0;
	for(i=0;i<n;i++){
		printf("Result:%d\n",fibnaci(i));
	}
}
