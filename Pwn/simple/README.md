# simple [150|62]
Simple game right?
```
nc challs.sieberrsec.tech 8862
```

```c
#include <stdio.h>
#include <stdlib.h>

// cc simple.c -o simple -fstack-protector-all
int main(void)
{
	puts("Want a flag? Just play until you win!");
	puts("Goal: Become a billionaire!");
	int account_value = 1000000;
	while (account_value < 1000000000) {
		printf("\nAccount value: $%d\n", account_value);
		puts("Commands:");
		puts("1. Withdraw money");
		puts("2. Deposit money");
		printf("Choose an option [1/2]: ");
		int option = 0;
		scanf("%d", &option);
		while (option != 1 && option != 2) {
			puts("Invalid option!");
			printf("Choose an option [1/2]: ");
			scanf("%d", &option);
		}
		if (option == 1) {
			printf("Amount to withdraw: ");
			int withdrawal = 0;
			scanf("%d", &withdrawal);
			account_value -= withdrawal;
		} else {
			puts("LOL no you are not allowed to deposit money. :(");
		}
	}
	printf("\nAccount value: $%d\n", account_value);
	system("cat flag");
	return 0;
}
```

_Author: chowgz_

