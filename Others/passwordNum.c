#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>

#define BUF 10

int main() {
  unsigned int sec;
  int nsec;
  double d_sec;

  struct timespec start_time, end_time;
  int offset = 32;
  char str[BUF];
  int i = 0;
  for (i = 0; i < 10; i++) {
    str[i] = 0x30 + i;
  }
  for (i = 0; i < BUF; i++) {
    printf("%c ", str[i]);
  }
  //sleep(10);
  int j,m,n,c;
  c = 1;
  // Record time.
  clock_gettime(CLOCK_REALTIME, &start_time);
  for (i = 0; i < BUF; i++) {
    for (j = 0; j < BUF; j++) {
      for (m = 0; m < BUF; m++) {
        for (n = 0; n < BUF; n++) {
          printf("%8d::%c%c%c%c\n", c, str[i], str[j], str[m], str[n]);
          c++;
        }
      }
    }
  }
  // Record time
  clock_gettime(CLOCK_REALTIME, &end_time);
  sec = end_time.tv_sec - start_time.tv_sec;
  nsec = end_time.tv_nsec - start_time.tv_nsec;

  d_sec = (double)sec + (double)nsec / (1000 * 1000 * 1000);

  printf("===\ntime: %f s\n", d_sec);
  return 0;
}
