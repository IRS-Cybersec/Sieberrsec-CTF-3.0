# malloc [400|400]
Can you somehow get the flag? Have fun!
```
nc challs.sieberrsec.tech 1470
```

```c
#include <unistd.h>

#include <stdio.h>
#include <stdlib.h>

// cc malloc.c -o malloc -fstack-protector-all
int main(void)
{
	// Variables
	int *arr; // int pointer to an array
	char *msg; // C-string to store your message
	size_t length = 0;
	
	// Welcome message
	puts("Welcome to Sieberrsec CTF!");
	
	// Allocates 123456 bytes of memory
	arr = (int *)malloc(123456);
	
	// Sets first element of arr to 1
	arr[0] = 1;
	
	// Leaks the memory address of arr
	printf("Leak: %p\n", arr);
	
	// Gets length of your message
	printf("Length of your message: ");
	scanf("%lu", &length);
	
	// Allocates memory to store your message as a C-string
	// +1 is to store the null-byte that ends the string
	msg = malloc(length + 1);
	
	// Reads length bytes of input into msg
	printf("Enter your message: ");
	read(0, msg, length);
	
	// Null-byte to end the string
	msg[length] = 0;
	
	// Write length bytes from msg
	write(1, msg, length);
	
	// Your goal: somehow make arr[0] == 0
	if (arr[0] == 0) {
		system("cat flag");
	}
	return 0;
}
```
_Author: chowgz_
