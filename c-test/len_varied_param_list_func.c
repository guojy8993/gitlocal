#include<stdio.h>
#include<stdarg.h>

double avg(int num,...){
	va_list valist;
	double sum = 0.0;
	int i;

	va_start(valist,num);
	for(i=0;i<num;i++){
		sum += va_arg(valist,int);
	}
	va_end(valist);
	return sum/num;
}

int main(){
	printf("Average of %d,%d,%d:%f",1,2,3,avg(1,2,3));	



}
