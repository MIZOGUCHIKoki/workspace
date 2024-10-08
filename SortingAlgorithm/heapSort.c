#include <stdio.h>
#include "sort.h"

void pushHeap(unsigned int heapTree[], unsigned int x, unsigned int size);
unsigned int deleteMaximum(unsigned int heapTree[], unsigned int size);
void pushHeapFromData(unsigned int data[], unsigned int heapTree[]);
void deleteMaximumFromData(unsigned int heapTree[], unsigned int data[]);

int main() {
	unsigned int data[dataSize], original[dataSize], heapTree[dataSize] = {0};
	createData(data, original);
	printData(data);
	pushHeapFromData(data, heapTree);
	deleteMaximumFromData(heapTree, data);
	printData(data);
	verifySort(data, original);
	return 0;
}


void pushHeapFromData(unsigned int data[], unsigned int heapTree[]) {
	unsigned int i;
	printDataVert(data);
	printf("push heap\n");
	for (i = 0; i < dataSize; i++) {
		pushHeap(heapTree, data[i], i);
	}
	printDataVert(heapTree);
}

void deleteMaximumFromData(unsigned int heapTree[], unsigned int data[]) {
	unsigned int i = dataSize - 1;
	printf("delete maximum\n");
	for (i = dataSize - 1; i > 0; i--) {
		data[i] = deleteMaximum(heapTree, i);
	}
	data[0] = deleteMaximum(heapTree, i);
	return;
}
