#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "sort.h"

void createData(unsigned int data[], unsigned int original[]) {
	unsigned int i;
	srand(time(NULL)); // set a random seed
	//srand(1);
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
		printf("%5d ", data[i]);
		if (i % 17 == 0) printf("\n");
	}
	printf("\n");
}


void verifySort(unsigned int data[], unsigned int original[]) {
	unsigned int i;
	unsigned int j = 0;
	unsigned int result[dataSize] = {0};
	for (i = 0; i < dataSize - 1; i++) {
		if (data[i] > data[i + 1]) {
			fprintf(stderr, "Sort Failed.\n data[%3d] <-> data[%3d]\n", i, i + 1);
			j = 1;
			break;
		}
	}
	if (j == 1) return;
	for (i = 0; i < dataSize; i++) {
		binarySearch(data, original[i], result, i);
	}
	for (i = 0; i < dataSize; i++) {
		if (original[i] != result[i]) {
			fprintf(stderr, "Binary search Failed\n");
			return;
		}
	}
	printf("Sort Success\n");
}

void swap(unsigned int data[], unsigned int index_1, unsigned int index_2) {
	unsigned int x = data[index_1];
	data[index_1] = data[index_2];
	data[index_2] = x;
	return;
}
