#include <stdio.h>
#include "sort.h"

void insertSort(unsigned int data[]);

int main() {
	unsigned int data[dataSize], original[dataSize];
	createData(data, original);
	printData(data);
	insertSort(data);
	printData(data);
	verifySort(data, original);
	return 0;
}

void insertSort(unsigned int data[]) {
	printf("--- Sorting ---\n");
	unsigned int i, j, x;
	for (i = 1; i < dataSize; i++) {
		j = i; 
		x = data[i];
		while(1) {
			if (j <= 0) break;
			if (data[j - 1] <= x) break;
			data[j] = data[j - 1]; // Shift elements to the left
			j--;
		}
		data[j] = x;
	}
	return;
}
