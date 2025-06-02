/*
  AUTHOR:      MIZUGUCHI Koki
  `- Affiliation: Kochi University of Technology

  Released under the MIT license
  Copyright (c) 2024 MIZOGUCHI Koki
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

unsigned short genRN(unsigned short total, int fd);
void deleteEmptyElement(unsigned short *array, unsigned short arrayLength);
void printArray(unsigned short *array, unsigned short arrayLength);

// Define temporary variable as Global variable
unsigned short i, j;

int main(int argc, char *argv[])
{
  if (argc != 3)
  {
    fprintf(stderr, "Usage: %s <Number of students in the class> <Number of students you want>\n", argv[0]);
    exit(1);
  }
  unsigned short size, total, counter;
  total = atoi(argv[1]);
  const unsigned short cTotal = total;
  size = atoi(argv[2]);
  counter = 0;
  if (size > total)
  {
    fprintf(stderr, "Enter a number less than %d in second argument\n", total);
    exit(1);
  }
  unsigned short num[total]; // Total number array
  unsigned short tmp; // Define temporary variable
  for (i = 0; i < total; i++) {
    num[i] = i + 1;
  }
  printf("Generate %d random number(s) from %d through %d\n", size, 1, total);

  printf("------+----------\n");
  printf("%-5s | %-8s\n", "ORDER", "Identity");
  printf("------+----------\n");


	int fd = open("/dev/random", O_RDONLY);
	if (fd == -1) {
		perror("open");
		exit(1);
	}
  while (1)
  {
    tmp = genRN(total, fd);                              // Generate a random number
    printf("%5d | %8d\n", counter + 1, num[tmp]);
    num[tmp] = 0;
    deleteEmptyElement(num, cTotal);
    counter++;
    total--;
    if (counter == size)
      break;
  }
  printf("------+----------\n");
	close(fd);
  return 0;
}

unsigned short genRN(unsigned short total, int fd)
{
	int random_number;
	if (read(fd, &random_number, sizeof(random_number)) != sizeof(random_number)) {
		perror("read");
		close(fd);
		exit(1);
	}
  return ((unsigned int)random_number % total);
}

void deleteEmptyElement(unsigned short *array, unsigned short arrayLength)
{
  unsigned short tmp[arrayLength];
  j = 0;
  for (i = 0; i < arrayLength; i++)
  {
    if (array[i] == 0)
      continue;
    tmp[j] = array[i];
    j++;
  }
  for (i = 0; i < arrayLength; i++) {
    array[i] = tmp[i];
  }
}

// The following methods are for DEBUG
void printArray(unsigned short *array, unsigned short arrayLength) {
  for (i = 0; i < arrayLength; i++) {
    printf("array[%d] = %d\n", i, array[i]);
  }
}
