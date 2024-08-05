#include <stdio.h>
#include "sort.h"

void pushHeap(unsigned int heapTree[], unsigned int x);
pushHeapFromData(unsigned int data[], unsigned int heapTree[]);

int main() {
	unsigned int data[dataSize], original[dataSize], heapTree[dataSize] = {0};
	createData(data, original);
	printData(data);
	pushHeapFromData(data, heapTree);
	return 0;
}


void pushHeapFromData(unsigned int data[], unsigned int heapTree[]) {

}
