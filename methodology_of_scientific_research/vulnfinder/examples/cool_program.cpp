#include <cstring>
#include <iostream>

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Usage: cool_program <input>\n";
        return 1;
    }

    char buffer[16];
    std::strcpy(buffer, argv[1]);
    std::cout << "You entered: " << buffer << "\n";
    return 0;
}

