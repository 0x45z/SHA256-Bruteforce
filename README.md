# SHA256 Bruteforce

This program performs a brute force attack on a SHA256 hash to reveal the pre-hashed plaintext. This is NOT a dictionary attack, thus no dictionary is required.  

## Usage
Arguments can be passed via the command line before running the program:

    Flags:

    -h  Show the help menu.

    -c  Specify the SHA256 Hash(es) to crack
    
    Optional:

    -l  Specify the maximum length to attempt to crack

    -s  Use only selected character sets. Usage:Lowercase = l, Uppercase = u, Numbers = n, Special Characters = s. (e.g. lnus = full character set)


    Example usage:
    python3 main.py -c 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 -l 8 -s lnus
