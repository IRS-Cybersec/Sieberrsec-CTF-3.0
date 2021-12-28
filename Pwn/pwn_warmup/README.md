# warmup
Just a warmup. `nc de.irscybersec.tk 3476`
```c
#include <stdio.h>
int main() {
    char input[32];
    char flag[32];
    // read flag file
    FILE *f = fopen("flag", "r");
    fgets(flag, 32, f);
    fclose(f);
    // read the user's guess
    fgets(input, 0x32, stdin);
    // if user's guess matches the flag
    if (!strcmp(flag,input)) {
        puts("Predicted!");
        system("cat flag");
    } else puts("Your flag was wrong :(");
}
```

Extra info if you're lost:
* https://ctf101.org/binary-exploitation/buffer-overflow/
* https://en.wikipedia.org/wiki/Null-terminated_string

N.B. please do not try to bruteforce the flag. Attempts at doing so will be taken as an attack on server infrastructure, and will leave you liable for disqualification.
