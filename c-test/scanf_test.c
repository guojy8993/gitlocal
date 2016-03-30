/*
 * @file scanf_test.c
 * @note This program displays usage of `scanf`
 */
#include<stdio.h>

int main(){
    int i;
    while(1){
    	printf("Enter A Number:\n");
    	scanf("%d",&i);
    	printf("Number %d entered\n",i);
    }    
}

