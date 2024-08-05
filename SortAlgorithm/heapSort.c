#include <stdio.h>
#include "sort.h"

void pushHeap(unsigned int heapTree[], unsigned int x, unsigned int size);
void pushHeapFromData(unsigned int data[], unsigned int heapTree[]);

int main() {
	unsigned int data[dataSize], original[dataSize], heapTree[dataSize] = {0};
	createData(data, original);
	printData(data);
	pushHeapFromData(data, heapTree);
	return 0;
}


void pushHeapFromData(unsigned int data[], unsigned int heapTree[]) {
	unsigned int i;
	printDataVert(heapTree);
	printf("push heap\n");
	for (i = 0; i < dataSize; i++) {
		pushHeap(heapTree, data[i], i);
	}
	printDataVert(heapTree);
}
