#!usr/bin/python
import argparse
import csv




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

    print(hashes)