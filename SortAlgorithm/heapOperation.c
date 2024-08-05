#include <stdio.h>
#include "sort.h"

void pushHeap(unsigned int heapTree[], unsigned int x, unsigned int size) {
	heapTree[size] = x;
	while (1) {
		if (size <= 0) break;
		if (heapTree[(size - 1) / 2] >= heapTree[size]) break;
		swap(heapTree, (size - 1) / 2, size);
		size = (size - 1) / 2;
	}
}

unsigned int deleteMaximum(unsigned int heapTree[], unsigned int size) {
	unsigned int return_value = heapTree[0];
	heapTree[0] = heapTree[size];
	heapTree[size] = 0;
	unsigned int k = 0;
	size--;
	// child element of data[k] is data[(k + 1) * 2 - 1], data[(k + 1) * 2]
	//printDataVert(heapTree);
	while (1) {
		if ((k + 1) * 2 - 1 > size) break; // Has no element
		if ((k + 1) * 2 - 1 == size) { // Has just 1 element
			if (heapTree[k] < heapTree[(k + 1) * 2 - 1]) {
				swap(heapTree, k, (k + 1) * 2 - 1);
				k = (k + 1) * 2 - 1;
			} else { break; }
		} else if ((k + 1) * 2 - 1 < size) { // Has 2 elements
			if (heapTree[(k + 1) * 2 - 1] > heapTree[k] || heapTree[(k + 1) * 2] > heapTree[k]) {
				if (heapTree[(k + 1) * 2 - 1] <= heapTree[(k + 1) * 2]) {
					swap(heapTree, (k + 1) * 2, k);
					k = (k + 1) * 2;
				} else {
					swap(heapTree, (k + 1) * 2 - 1, k);
					k = (k + 1) * 2 - 1;
				}
			} else { break; }
		}
	}
	//printDataVert(heapTree);
	return return_value;
}
