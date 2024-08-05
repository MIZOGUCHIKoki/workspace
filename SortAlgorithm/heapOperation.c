#include <stdio.h>
#include "sort.h"

void pushHeap(unsigned int heapTree[], unsigned int x, unsigned int size) {
	heapTree[size] = x;
	while (1) {
		if (size <= 0) break;
		if (heapTree[size / 2] >= heapTree[size]) break;
		swap(heapTree, size / 2, size);
		size = size / 2;
	}
}

unsigned int deleteMaximum(unsigned int heapTree[], unsigned int size) {
	unsigned int return_value = heapTree[0];
	heapTree[0] = heapTree[size];
	heapTree[size] = 0;
	size--;
	unsigned int k = 1;
	while (1) {
		if (k * 2 > size) break; // Has any child nodes?
		if (k * 2 == size) { // Has just 1 child.
			if (heapTree[k - 1] > heapTree
		}
	}
	return return_value;
}
