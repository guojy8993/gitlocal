#include<stdio.h>
#include<string.h>

struct Book{
	char title[50];
	char author[50];
	char subject[100];
	int book_id;
};

int main(){
	int i = 0;
	struct Book books[100]; 
	for(i=0;i<100;i++){
		strcpy(books[i].title,"Title");
		strcpy(books[i].author,"Author");
		strcpy(books[i].subject,"SubJ");
		books[i].book_id = i;
	}
	printf("Books already on shleves .\n");
	for(i=0;i<100;i++){
		printf("Book %s,subject %s,author %s,id %d \n",books[i].title,books[i].subject,books[i].author,books[i].book_id);
	}
	return 0;

}
