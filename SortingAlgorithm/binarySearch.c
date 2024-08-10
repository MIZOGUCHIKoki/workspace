#include <stdio.h>
#include "sort.h"

void binarySearch(unsigned int data[], unsigned int x, unsigned int result[], unsigned int index) {
	unsigned int i, j = 0;
	unsigned int left = 0, right = dataSize - 1;
	unsigned int mid = (left + right) / 2;
	for (i = 0; i < dataSize; i++) {
		while(left < right) {
			if (data[mid] == x) {
				result[index] = x;
				break;
			}
			else if (data[mid] < x) left = mid + 1;
			else right = mid - 1;
			mid = (left + right) / 2;
		}
		if (data[mid] == x) {
			result[index] = x;
		}
		else return;
	}
	return;
}
