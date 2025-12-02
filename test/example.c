#include <string.h>
#include <stdio.h>

void bad() {
    char buffer[10];
    strcpy(buffer, "AAAAAAAAAAAAAAAA");
}
