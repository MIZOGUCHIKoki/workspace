/*
  @AUTHOR:      MIZUGUCHI Koki
    Affiliation: Kochi University of Technology

  Released under the MIT license
  (c) 2024 MIZOGUCHI Koki
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int genRN(int total);

int main(int argc, char *argv[]) {
  if (argc != 3) {
    fprintf(stderr, "Usage: %s <Number of students in the class> <Number of students you want>\n", argv[0]);
    exit(1);
  }
  unsigned short size, total, counter;
  total = atoi(argv[1]);
  size = atoi(argv[2]); 
  counter = 0;
  if (size >= total) {
    fprintf(stderr, "Enter a number less than %d in second argument\n", total);
    exit(1);
  }
  unsigned short ls[size];
  printf("Generate %d random numbers from %d through %d\n", size, 1, total);
  unsigned short i, j;


  printf("------+----------\n");
  printf("%-5s | %-8s\n", "ORDER", "Identity"); 
  printf("------+----------\n");

  unsigned short tmp, flag;
  while(1) {
    flag = 0;
    srand((unsigned int)time(NULL)); // set the random seed
    tmp = genRN(total); // Generate a random number
    for (i = 0; i < counter; i++) {
      if (ls[i] == tmp) {
        flag = 1;
        break;
      }
    }
    if (flag == 1) continue; // if there is a duplicated number, back to the begining of the while process.
    ls[counter] = tmp;
    printf("%5d | %5d\n", counter + 1, ls[counter]);
    counter++;
    if (counter == size) break;
  }
  printf("------+----------\n");
  return 0;
}

int genRN(int total) {
  return (rand() % total) + 1;
}
