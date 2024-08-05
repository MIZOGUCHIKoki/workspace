#include <stdio.h>
#include "sort.h"

void selectionSort(unsigned int data[]);

int main() {
	unsigned int data[dataSize], original[dataSize];
	createData(data, original);
	printData(data);
	selectionSort(data);
	printData(data);
	verifySort(data, original);
	return 0;
}

void selectionSort(unsigned int data[]) {
	printf("--- Sorting ---\n");
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
	return;
}
