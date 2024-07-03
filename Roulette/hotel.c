#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
 unsigned int a = 0;
 unsigned int b = 0;
 unsigned int parm = atoi(argv[1]);
 while(1) {
   srand(b + parm);
   if ( b == parm ) break;
   b++;
   a = (unsigned int)rand();
   printf("%10d\n", a);
   switch((unsigned int)(a % 3)) {
     case 0:
      printf("%3d : 桜スカイホテル 柏\n", b);
      break;
     case 1:
      printf("%3d : 三井ガーデンホテル\n", b);
      break;
     case 2:
      printf("%3d : KSEA\n", b);
      break;
     default:
      printf("ERROR\n");
      break;
   }
 }
}
