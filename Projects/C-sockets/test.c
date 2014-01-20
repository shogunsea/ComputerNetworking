#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main(void){
   char *s = "string";
   char *t = "-27993";
   int len = strlen (s);
  printf("1 is equal to 1: %i\n",1==1);
  printf("1 && 1: %i\n",1&&1);
  printf("1 && 0: %i\n",1&&0);
  // printf("1 is equal to 1: %i\n",1==1);
  // printf("1 is equal to 1: %i\n",1==1);

  printf("string as port: %i\n",(int)strtol(s,NULL,10));
  printf("27993 as port: %i\n",(int)strtol(t,NULL,10));
  printf("-27993's first char: %c\n", t[0]);

  if(1){
  	printf("this is inside if(1) conditional.\n");
  }
  if(0){
  	printf("this is inside if(0) conditional.\n");
  }
   printf("len is: %i\n", len);
   return 1;
}

