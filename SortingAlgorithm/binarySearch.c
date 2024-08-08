#include <stdio.h>
#include "sort.h"

unsigned int binarySearch(unsigned int data[], unsigned int x) {
	unsigned int i, j = 0;
	unsigned int left = 0, right = dataSize - 1;
	unsigned int mid = (left + right) / 2;
	for (i = 0; i < dataSize; i++) {
		while(left < right) {
			if (data[mid] == x) return 0;
			else if (data[mid] < x) left = mid + 1;
			else right = mid - 1;
			mid = (left + right) / 2;
		}
		if (data[mid] == x) return 0;
		else return 1;
	}
	return 0;
}
