//usr/bin/gcc "$0" -o "$0.o"; exit
#include <stdio.h>
int main() {
    char input[32];
    char flag[32];
    FILE *f = fopen("flag", "r");
    fgets(flag, 32, f);
    fclose(f);
    fgets(input, 0x32, stdin);
    if (!strcmp(flag,input)) {
        puts("Predicted!");
        system("cat flag");
    } else puts("Your flag was wrong :(");
}
