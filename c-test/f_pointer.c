/*
 * @file    f_pointer.c
 * @date    2015/12/29
 * @author  guojy
 * @desc    This program show the useage of pointer-type return-value 
 *          in function defination.
 */

#include<stdio.h>
#include<stdlib.h>

int *sum(int a,int b);
int *sum(int a,int b)
{
	int *p;
	int result = a + b;
	p = &result;
	return p;
}

int main(int argc,char **argv)
{
	printf("Sum of %d and %d : %d\n",2,3,*(sum(2,3)));
	
}
