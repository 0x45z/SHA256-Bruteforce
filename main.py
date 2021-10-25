#!usr/bin/python
import argparse
import csv
import time
from itertools import chain, product
import hashlib

char1 = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
char2 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
char3 = ('0','1','2','3','4','5','6','7','8','9')
char4 = ('!', '@', '%', ':', '£', '$', '-', '*', '/', ';', '|', '#', '.', ',')
current_char = ()

class bruteForce():
    def __init__(self):
        self.time = time.time() # initialise timer

    def main(self, passw_hash):
        # then call hash function, check if equal
        for attempt in bruteForce.crack(current_char, max_length): # for each attempt in crack function
            if bruteForce.hash(attempt) == passw_hash: # compare hashed value of guess with hash value
                time_taken = ('{:.2f}s'.format(time.time() - self.time)) # get time taken to complete within 2 decimal places
                return passw_hash, attempt, time_taken, True # return hash, plain text password and time taken
        return passw_hash, 'Character set exhausted. Password not found.', ('{:.2f}s'.format(time.time() - self.time)), False # if password not found

    @staticmethod
    def crack(charset=char1+char3+char4,maxlength=5):
        return (''.join(candidate)
                # return every possible combination of the character set 'charset', up to length 'maxlength'
                for candidate in chain.from_iterable(product(charset, repeat=i)
                for i in range(1, maxlength + 1)))

    @staticmethod
    def hash(guess):
        return hashlib.sha256(guess.encode()).hexdigest() # hash and return the guess



def get_csv_hashes():
    csv_hashes = []
    with open('sha256_hashes.csv', 'r') as file:
        data = csv.DictReader(file)
        for lines in data:
            csv_hashes.append(lines['hash']) # save hashes in csv to the list csv_hashes
    return csv_hashes

def main():
    start_time = time.time() # get start time
    results = {}
    cracked = 0
    print('[Status]: %s Hashes received\n' % len(hashes))
    for hash in hashes:
        print(f'[Status]: Attempting to decrypt hash {hash}\n')
        data = bruteForce().main(hash) # pass hash to bruteForce class and save returned values
        if data[3] == True: # if hash successfully cracked
            print(f'[Cracked]: {data[0]}:{data[1]} Time elapsed: {data[2]}\n') # print the hash, plaintext and time taken
            cracked+=1 # increment the counter
        else:
            print(f'[Error]: {data[0]} {data[1]} Time elapsed: {data[2]}\n')
        results[data[0]] = list() # create list in dictionary with the password hash as key
        results[data[0]].extend(data[1:]) # add the rest of the data to the dictionary under the hash as the key
    total_taken = ('{:.2f}s'.format(time.time() - start_time)) # get total time elapsed to 2 dp
    print('[Status]: Process complete.\n')
    print(f'Cracked {cracked}/{len(hashes)} hashes in {total_taken}\n')
    print('Hash                              Plaintext        Time taken')
    for hash in hashes:
        if not results[hash][2]: # if hash not cracked
            continue
        print(hash[:30]+'...', results[hash][0], (' '*(15-len(results[hash][0]))),results[hash][1])
        """
        ^^ print first 30 characters of hash, plaintext value, the appropriate amount of spaces so that
        the value of time taken aligns with the time taken column and finally time taken.
        this is done so that the text is formatted for the generic console window size.
        """



if __name__ == "__main__":
    # parse command line for inputted hashes
    parser = argparse.ArgumentParser(description='Decrypt SHA256 hashes using a brute force attack',)
    parser.add_argument('-c', '--crack', type=str, metavar='', required=False, help='Enter SHA256 Hash(es) to brute force', nargs='*')
    parser.add_argument('-l', '--max-length', type=int, metavar='', required=False, default=5, help='Enter the maximum length to attempt to crack')
    parser.add_argument('-s', '--charset', type=list, metavar='', required=False, default=['l','n','s'], help='Use only selected character sets. Usage:Lowercase = l, Uppercase = u, Numbers = n, Special Characters = s. e.g. lnus = full character set')
    args = parser.parse_args()

    hashes = []

    if args.crack:  # if any hashes were inputted
        hashes += args.crack  # store inputted hashes in a list
    else:
        print('No hashes received via command line')

    try:
        hashes += get_csv_hashes()  # add hashes in csv file to the hashes list
    except Exception as error:
        if not args.crack:  # if hashes were not received from cli or csv file
            print('Error: no hashes received via command line or csv file')
            exit()
        print('Error: %s. Using only hashes received via command line' % error)

    if args.max_length: # if user inputted a max word length
        max_length = args.max_length

    if args.charset: # if user inputted specific character set(s) to be used
        if 'l' in args.charset:
            current_char += char1 # add lower case charset to current charset
        if 'u' in args.charset:
            current_char += char2 # add upper case charset to current charset
        if 'n' in args.charset:
            current_char += char3 # add number charset to current charset
        if 's' in args.charset:
            current_char += char4 # add special characters charset to current charset

    main()
