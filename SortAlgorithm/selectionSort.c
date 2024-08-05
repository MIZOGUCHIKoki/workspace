#include <stdio.h>
#include "sort.h"

unsigned int selectionSort(unsigned int data[]);

int main() {
	unsigned int i, j;
	unsigned int data[dataSize], original[dataSize];
	createData(data, original);
	printData(data);
	if ((j = selectionSort(data)) != 0) {
		fprintf(stderr, "selection Sorf failed. Error %d\n", j);
	} else {
		printf("The data has sorted.\n");
	}
	printData(data);
	verifySort(data, original);
	return 0;
}

unsigned int selectionSort(unsigned int data[]) {
	unsigned int max;
	unsigned int max_indent;
	unsigned int i, j;
	for (i = dataSize - 1; i > 0; i--) {
		max = data[0];
		max_indent = 0;
		for (j = 0; j <= i; j++) {
			if (max <= data[j]) {
				max_indent = j;
				max = data[j];
			}
		}
		data[max_indent] = data[i];
		data[i] = max;
	}
	return 0;
}
