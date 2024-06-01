#include <stdio.h>

void arrayMethods(unsigned short *array, unsigned short arrayLength) {
  printf
int main() {
  int arrayI[10];
  unsigned short arrayS[10];
  unsigned short arrayTMP[10];
  unsigned short j;
  int i;
  for (i = 0; i < 10; i++) {
    arrayI[i] = i;
    printf("arrayI[%d] = %d\n", i, arrayI[i]);
    arrayS[i] = i;
    printf("arrayS[%d] = %d\n", i, arrayS[i]);
  }
  for (j = 0; j < 10; j++) {
    arrayI[j] = j;
    printf("arrayI[%d] = %d\n", j, arrayI[j]);
    arrayS[j] = j;
    printf("arrayS[%d] = %d\n", j, arrayS[j]);
  }

  unsigned short tmp1 = 100;
  int tmp2 = 100;
  printf("SHORT PD: %d, SHORT PU: %u, INT PD: %d\n", tmp1, tmp1, tmp2);

  for (j = 0; j < 10; j++) {
    arrayTMP[j] = arrayS[j];
    printf("arrayTMP[%d] = %d\n", j, arrayTMP[j]);
  }
  return 0;
}

