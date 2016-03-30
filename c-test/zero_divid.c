#include<stdio.h>
#include<stdlib.h>

main(){
	int dividend = 20;
	int divisor = 0;
	// int divisor = 5;
	int quotient;
	
	if(divisor == 0){
		// fprintf(stderr,"Divison by Zero ! Exit .");
		exit(EXIT_FAILURE);
	}
	quotient = dividend / divisor ;
	fprintf(stderr,"Value of quotient: %d\n",quotient);
	
	exit(EXIT_SUCCESS); 
}
