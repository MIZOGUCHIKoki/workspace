#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct mileage {
 unsigned int updated;
 unsigned short int mile;
 unsigned short int lsp;
 unsigned short int board;
};

struct flight {
  unsigned int date;
  char dep[4];
  unsigned short int dep_time;
  char arr[4];
  unsigned short int arr_time;
  char iata[3];
  unsigned short int code;
  char class[2];
  char booking[7];
};

size_t size_formatted_date = 19;
size_t size_flight_data = 44;

void print_mileage(struct mileage *m);
void print_date(unsigned int date, char *result);
void error_handling(FILE *fp1, FILE *fp2);
unsigned short int mileage_p(struct mileage *mileage, FILE *fp_mileage);
short int count_flight(FILE *fp_flight);
unsigned short int flights_p(struct flight *flight, FILE *fp_flights, short int flights);

int main() {
  FILE *fp_mileage = fopen("mileage.csv", "r");
  if (fp_mileage == NULL){
     perror("Cannot open mileage.csv");
     return 1;
  }
  FILE *fp_flights = fopen("flights.csv", "r");
  if (fp_flights == NULL) {
    fclose(fp_mileage);
    perror("Cannot open flights.csv");
    return 1;
  }
  struct mileage mileage;
  if (mileage_p(&mileage, fp_mileage) == 1) {
    perror("mileage_p function call failed");
    error_handling(fp_mileage, fp_flights);
    return 1;
  }
  short int flights;
  if ((flights = count_flight(fp_flights)) == -1) {
    perror("count_flight function call failed");
    error_handling(fp_mileage, fp_flights);
    return 1;
  }
  struct flight flight[flights];
  flights_p(flight, fp_flights, flights);
  
  int i, j;
  char result[size_formatted_date];
  printf("\n");
  for (i = 0; i < flights; i++) {
    print_date(flight[i].date, result);
    printf("%10s | ", result);
    printf("%3s | ", flight[i].dep);
    printf("%3s | ", flight[i].arr);
    printf("\n");
  }

  fclose(fp_flights);
  return 0;
}

void error_handling(FILE *fp1, FILE *fp2) {
  fclose(fp1);
  fclose(fp2);
}

void print_mileage(struct mileage *m) {
  char formatted_date[size_formatted_date];
  print_date((*m).updated, formatted_date);
  printf("%8s", "updated");
  printf("  %s\n", formatted_date);
  printf("%8s", "MILE");
  printf("  %hu\n", (*m).mile);
  printf("%8s", "LSP");
  printf("  %hu\n", (*m).lsp);
  printf("%8s", "Boarding");
  printf("  %hu times/year\n", (*m).board);
}

void print_date(unsigned int date, char *result) {
  /* 
    e.g., date = 20250701
    sizeof(result) = size_formatted_date
  */
  unsigned short int year = date / 10000; // e.g., 2025
  unsigned short int month = (date - year * 10000) / 100; // e.g., 7
  unsigned short int day = (date - year * 100) % 100;
  const char *months[] = {
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    };
  if (month >=1 && month <= 12) {
      snprintf(result, size_formatted_date, "%hu %s, %hu", day, months[month - 1], year);
  } else {
    printf("Invalid month: %d\n", month);
  }
}  

unsigned short int mileage_p(struct mileage *mileage, FILE *fp_mileage) {
  char formatted_date[size_formatted_date];
  char line[128];
  char key[64];
  char value[64];

  unsigned int updated = 0;
  unsigned short int mile = 0;
  unsigned short int lsp = 0;

  size_t ret, ret2;

  unsigned short int i, j;
  while (1) {
    memset(key, 0, 64);
    memset(value, 0, 64);
    if (fgets(line, sizeof(line), fp_mileage) == 0)
      break;
    line[ret2 = strcspn(line, "\n")] = '\0'; // remove \n
    ret = strcspn(line, ","); // ret is index of camma
    
    //fputs(line, stdout);
    for (i = 0; i < ret; i++) {
      key[i] = line[i];
    }
    for (j = 0, i = ret + 1; i < ret2; i++, j++) {
      value[j] = line[i];
    }
    
    if (strcmp(key,"updated") == 0) {
     (*mileage).updated = (unsigned int)atoi(value);
    } else if (strcmp(key, "mile") == 0) {
     (*mileage).mile = (unsigned short int)atoi(value);
    } else if (strcmp(key, "lsp") == 0) {
      (*mileage).lsp = (unsigned short int)atoi(value);
    } else if (strcmp(key, "board") == 0) {
      (*mileage).board = (unsigned short int)atoi(value);
    } else {
      perror("mileage property error");
      return 1;
    }
  }

  print_mileage(mileage);
  fclose(fp_mileage);
  return 0;
}

short int count_flight(FILE *fp_flights) {
  short int counter = 0;
  char line[size_flight_data];
  while (1) {
    if (fgets(line, sizeof(line), fp_flights) == 0)
      break;
    counter++;
  }
  rewind(fp_flights);
  // printf("Booked Flights: %d flight(s)\n", counter);
  return counter;
}

unsigned short int flights_p(struct flight *flight, FILE *fp_flights, short int flights) {
  unsigned short int counter = (unsigned short int)flights;
  char line[size_flight_data];
  char date[8];
  char time[4];
  char airport[3];
  char iata[2];
  char code[3];
  char fare[1];
  char booking[6];
  int i, j = 0;
  unsigned int tmp;
  size_t ret2;
  char *token;
  while (1) {
    i = 0;
    if (counter < 0) {
      perror("struct flight may overflow buffer");
      return 1;
    }
    if (fgets(line, sizeof(line), fp_flights) == 0) {
      break;
    }
    line[ret2 = strcspn(line, "\n")] = '\0'; // remove \n
    token = strtok(line, ",");
    while (1) {
      if (token == 0)
        break;
      //printf("token: %s\n", token);
      //printf("`--%d-%d\n", j, i);
      switch (i) {
        case 0:
          flight[j].date = (unsigned int)atoi(token);
          break;
        case 1:
          flight[j].dep_time = (unsigned short int)atoi(token);
          break;
        case 2:
          flight[j].arr_time = (unsigned short int)atoi(token);
          break;
        case 3:
          strncpy(flight[j].dep, token, 3);
          flight[j].dep[sizeof(flight[j].dep) - 1] = '\0';
          break;
        case 4:
          strncpy(flight[j].arr, token, 3);
          flight[j].arr[sizeof(flight[j].arr) - 1] = '\0';
          break;
        case 5:
          strncpy(flight[j].iata, token, 2);
          flight[j].iata[sizeof(flight[j].iata) - 1] = '\0';
          break;
        case 6:
          flight[j].code = (unsigned short int)atoi(token);
          break;
        case 7:
          strncpy(flight[j].class, token, 1);
          flight[j].class[sizeof(flight[j].class) - 1] = '\0';
          break;
        case 8:
          strncpy(flight[j].booking, token, 6);
          flight[j].booking[sizeof(flight[j].booking) - 1] = '\0';
          break;
        default:
          perror("Invalid flights data");
          return 1;
      }
      i++;
      token = strtok(NULL, ",");
    }
    counter--;
    j++;
  }
  return 0;
}
