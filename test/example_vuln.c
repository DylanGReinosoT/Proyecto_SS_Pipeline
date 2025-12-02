#include <string.h>

void bad_function() {
    char buffer[10];
    strcpy(buffer, "AAAAAAAAAAAAAAAAAAAAAAAAA"); // Overflow
}
