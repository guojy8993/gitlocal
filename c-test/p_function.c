/*
 * @file   p_function.cr
 * @data   2015/12/29
 * @author guojy
 * @desc   This program displays how to use function pointer
 */

#include<stdio.h>
#include<stdlib.h>

int sum(int a,int b);
int sum(int a,int b)
{
	return a+b;
}
int (*pfunc)(int,int);


int main(int argc,char **argv)
{
	printf("sum(%d,%d) = %d\n",2,3,sum(2,3));
        pfunc = &sum;
	printf("(*pfunc)(%d,%d) = %d\n",2,5,(*pfunc)(2,5));
        printf("pfunc(%d,%d) = %d\n",2,5,pfunc(2,5));	
}

