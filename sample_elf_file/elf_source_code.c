#include <string.h>
#include <stdio.h>
void swap(int *a, int *b){
    *a^=*b;
    *b^=*a;
    *a^=*b;
}

int main(){
    int a,b;
    int *pa=&a;
    int* pb=&b;
    float c;
    char str_1[6]="Hello ";
    char str_2[6]="World!";
    char str_3[13]={};
    a=1;
    b=2;
    memcpy(str_3,str_1,6);
    memcpy(str_3+6,str_2,6);
    printf("%s\n",str_3);
    printf("A is : %d\n",*pa);
    printf("B is : %d\n",*pb);
    printf("Do Swap.\n");
    swap(pa,pb);
    printf("A is : %d\n",*pa);
    printf("B is : %d\n",*pb);

return 0;
}
