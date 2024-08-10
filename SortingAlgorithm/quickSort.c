#include <stdio.h>
#include "sort.h"

void quickSort(unsigned int data[], unsigned int left, unsigned int right);
unsigned int partition(unsigned int data[], unsigned int left, unsigned int right);

int main() {
	unsigned int data[dataSize], original[dataSize];
	createData(original, data);
	//printf("ORIGINAL\n >> ");
	//printData(data);
	//printf("\n");
	//printf(">> CALL(0) quickSort(left = %u, right = %u)\n", 0, dataSize - 1);
	printf("--- Sorting ---\n");
	quickSort(data, 0, dataSize - 1);
	//printData(data);
	verifySort(data, original);
	return 0;
}

void quickSort(unsigned int data[], unsigned int left, unsigned int right) {
	//printDataVert(data);
	if (left < right) {
		unsigned int pivod_index = partition(data, left, right);
		//printf("pivod_index = %d\n", pivod_index);
		//printf(">> CALL(1) quickSort(left = %u, right = %u)\n", left, pivod_index - 1);
		quickSort(data, left, pivod_index - 1);
		//printf(">> CALL(2) quickSort(left = %u, right = %u)\n", pivod_index + 1, right);
		quickSort(data, pivod_index + 1, right);
	}
}

unsigned int partition(unsigned int data[], unsigned int left, unsigned int right) {
	unsigned int mid = (left + right) / 2;
	unsigned int k;
	// select the median value among {data[left], data[mid], data[right]}
	if ((data[left] >= data[mid] && data[left] <= data[right]) || (data[left] >= data[right] && data[left] <= data[mid])) {k = left;}
	else if ((data[mid] >= data[left] && data[mid] <= data[right]) || (data[mid] >= data[right] && data[mid] <= data[left])) {k = mid;}
	else {k = right;}
	
	//printf("CALLED partition(), Data[%u] = %u is selected as a pivod value\n", k, data[k]);
	swap(data, k, right);
	int i = left, j = right - 1;
	//printDataVert(data);
	while (1) {
		if (i > j) { 
			//printf("Break while\n i = %u, j = %u\n", i, j);
			break;
		}
		//printf("debug point(0)\n i = %u, j = %u\n", i, j);
		while (data[i] < data[right]) {i++;}
		//printf("debug point(1)\n i = %u, j = %u\n", i, j);
		while (data[j] >= data[right] && j >= i && j > 0) {j--;}
		//printf("debug point(2)\n");
		if (i < j) {
			swap(data, i, j);
			//printf("swapped data[%u] <-> data[%u]\n -> ", i, j);
			//printDataVert(data);
		}
	}       
	//printf("swapped as final process\n i = %u, j = %u\n", i , j);
	swap(data, i, right); // set pivod value to mid of the set.
	//printDataVert(data);
	//printf("\n");
	return i; // return the pivod value location
}
