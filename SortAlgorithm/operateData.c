#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "sort.h"

void createData(unsigned int data[], unsigned int original[]) {
	unsigned int i;
	srand(time(NULL)); // set a random seed
	for (i = 0; i < dataSize; i++) {
		data[i] = (unsigned int)(rand() % dataSize);
		original[i] = data[i];
	}
}

void printData(unsigned int data[]) {
	unsigned int i;
	for (i = 0; i < dataSize; i++) {
		printf("data[%2d] = %2d\n", i, data[i]);
	}
}

void printDataVert(unsigned int data[]) {
	unsigned int i;
	for (i = 0; i < dataSize; i++) {
		printf("%2d ", data[i]);
	}
	printf("\n");
}


void verifySort(unsigned int data[], unsigned int original[]) {
	unsigned int i;
	unsigned int j = 0;
	for (i = 0; i < dataSize - 1; i++) {
		if (data[i] > data[i + 1]) {
			fprintf(stderr, "Sort Failed\n");
			j = 1;
			break;
		}
	}
	if (j == 1) return;
	for (i = 0; i < dataSize; i++) {
		if (binarySearch(data, original[i])) {
			fprintf(stderr, "binarySearch Failed\n");
			return;
		}
	}
	printf("Sort Success\n");
}

