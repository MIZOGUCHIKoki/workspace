#include <stdio.h>

int prime_factorization(int args[], int num);
void copy_array(int array_origin[], int array[], int size);
void print_array(int array[], int size);

int main() {
	int a, b, min, max, i, j;
	int k[1001], l[1001], k_copy[1001], l_copy[1001];
	for (;;) {
		for (;;) {
			printf("a = ");
			i = scanf("%d", &a);
			if (i != 1) {
				printf("数字を入力してください\n");
				while ((a = getchar()) != '\n') ; // Empty buffer a.
				continue;
			} else if (a < 2 || a > 1000) {
				printf("2以上1000以下の数値を入力してください\n");
			} else break; // Success to enter.
		}

		for (;;) {
			printf("b = ");
			i = scanf("%d", &b);
			if (i != 1) {
				printf("数字を入力してください\n");
				while ((b = getchar()) != '\n') ; // Empty buffer b.
				continue;
			} else if (b < 2 || b > 1000) {
				printf("2以上1000以下の数値を入力してください\n");
			} else break; // Success to enter.
		}

		if (a == b) {
			printf("異なる数字を入力してください\n");
			continue;
		} else break;
	}
	int num_a = prime_factorization(k, a);
	copy_array(k, k_copy, num_a);
	printf("a(%4d) の素因数 : ", a);
	print_array(k, num_a); // 素因数を見てみる
	int num_b = prime_factorization(l, b);
	copy_array(l, l_copy, num_b);
	printf("b(%4d) の素因数 : ", b);
	print_array(l, num_b); // 素因数を見てみる


	max = 1;
	i = 0; j = 0;
	/* 
		最大公約数を求める．
		二つのコピーされた配列k_copy, l_copyから，共通部分をとる．
		その共通部分を1つづつ掛けたものが最大公約数となる．
	*/
	for (i = 0; i < num_a; i++) {
		if (k_copy[i] == 0) continue;
		for (j = 0; j < num_b; j++) {
			if (l_copy[j] == 0) continue;
			if (k_copy[i] == l_copy[i]) {
				max = max * k_copy[i];
				k_copy[i] = 0;
				l_copy[j] = 0;
				break;
			}
		}
	}
	printf("%d と %d の最大公約数は%d\n", a, b, max);

	/*
		最小公倍数を求める．
	*/

	// 配列の初期化
	copy_array(k, k_copy, num_a);
	copy_array(l, l_copy, num_b);
	// 素因数の和集合を考える
	int u_size = num_a + num_b;
	int u[u_size];
	for (i = 0; i < num_a; i++) {
		u[i] = k[i];
	}
	for (j = 0; j < num_b; j++) {
		u[j + num_a] = l[j];
	}



	return 0;
}

/*
	配列argsに，numを素因数分解した値を格納する関数．
	戻り値は，配列のサイズ
*/
int prime_factorization(int args[], int num) {
	int i = 2;
	int index = 0, flag = 0;
	for (;;) {
		if (flag) { // 素因数が見つかった時
			i = 2;
			flag = 0;
		}
		if (num % i == 0) {
			args[index] = i;
			index++;
			num = num / i;
			flag = 1; // 素因数見つかりましたよFlag
			continue;
		}
		i++;
		if (num == 1) break;
	}
	return index;
}

/*
	配列をコピーする関数．
	array_originがコピー元，arrayがコピー先，sizeは配列サイズ．
*/
void copy_array(int array_origin[], int array[], int size) {
	int i;
	for (i = 0; i < size; i++) {
		array[i] = array_origin[i];
	}
}

// デバッグ用：配列をプリントする関数
void print_array(int array[], int size) {
	int i = 0;
	for (i = 0; i < size; i++) {
		printf("%3d ", array[i]);
	}
	printf("\n");
}
