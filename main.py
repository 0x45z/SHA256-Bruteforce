#!usr/bin/python
import argparse
import csv
import time
from itertools import chain, product
import hashlib

char1 = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
char2 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
char3 = ('0','1','2','3','4','5','6','7','8','9')

class bruteForce():
    def __init__(self):
        self.time = time.time() # initialise timer

    def main(self, passw_hash):
        # then call hash function, check if equal
        for attempt in bruteForce.crack(char1,5): # for each attempt in crack function
            if bruteForce.hash(attempt) == passw_hash: # compare hashed value of guess with hash value
                time_taken = ('{:.2f}s'.format(time.time() - self.time)) # get time taken to complete within 2 decimal places
                return passw_hash, attempt, time_taken # return hash, plain text password and time taken
        return passw_hash, 'Character set exhausted. Password not found.', ('{:.2f}s'.format(time.time() - self.time)) # if password not found

    @staticmethod
    def crack(charset,maxlength=5):
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



if __name__ == "__main__":
    # parse command line for inputted hashes
    parser = argparse.ArgumentParser(description='Brute force SHA256 hash')
    parser.add_argument('-c', '--crack', type=str, metavar='', required=False, help='Enter SHA256 Hash(es) to brute force', nargs='*')
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

    print(bruteForce().main(hashes[0]))