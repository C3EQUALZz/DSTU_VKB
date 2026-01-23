import os
import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: sassy program <host>")
        return

    host = sys.argv[1]
    os.system("ping -c 1 " + host)  # Unsanitized user input


if __name__ == "__main__":
    main()

