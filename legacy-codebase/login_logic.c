#include <string.h>

/**
 * We wrap the variables in a struct to encourage the compiler 
 * to place 'is_authenticated' immediately after 'password_buffer' 
 * in memory, though even with a struct, padding can occur.
 */
#pragma pack(push, 1)  // Tells the compiler: "No padding, pack tightly!"
struct login_data {
    char password_buffer[8];
    int is_authenticated;
    char padding[64]; // This "catches" the extra overflow so it doesn't hit the Return Address
};
#pragma pack(pop)

int verify_login(const char *input_password) {
    struct login_data data;
    data.is_authenticated = 0; // Initialize to locked
    
    // VULNERABLE STEP: 
    // strcpy does not check if input_password fits in the 8-byte buffer.
    // If input is "AAAAAAAAAAAA", it fills the buffer and spills into is_authenticated.
    strcpy(data.password_buffer, input_password);

    // LEGITIMATE CHECK:
    // Even if this check fails, is_authenticated might already be non-zero 
    // due to the overflow above.
    if (strcmp(data.password_buffer, "secret") == 0) {
        data.is_authenticated = 1;
    }

    return data.is_authenticated;
}