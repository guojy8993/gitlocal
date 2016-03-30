#include<stdio.h>
#include<string.h>

struct Book{
	char title[50];
	char author[50];
	char subject[100];
	int book_id;
};

void printBook(struct Book *book){
	printf("BookTitle:%s,Book_id:%d\n",book->title,book->book_id);
}

int main(){
	struct Book Book1,Book2;
	strcpy( Book1.title, "C Programming");
	strcpy( Book1.author, "Nuha Ali"); 
	strcpy( Book1.subject, "C Programming Tutorial");
	Book1.book_id = 6495407;
	
	strcpy( Book2.title, "Telecom Billing");
   	strcpy( Book2.author, "Zara Ali");
   	strcpy( Book2.subject, "Telecom Billing Tutorial");
   	Book2.book_id = 6495700;

	printBook(&Book1);
	printBook(&Book2);	
}
