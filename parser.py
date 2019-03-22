#!/usr/bin/env python

"""
USAGE:

$ parser.py cloud 1000
$ parser.py on-premise 2000
"""

import os
import sys

EXTENSION = ".csv"
TEST_FOLDER = "tests"
NEW_DIRECTORY = "parsed"
FILES_TO_PARSE = [
    'aggregate_report'
]

# Creates a new directory
def create_folder(directory): 
    if not os.path.exists(directory):
        os.makedirs(directory)

# Writes header line into a file
def write_headers_file(file_path, headers):
    with open(file_path, "w") as f:
        f.write(headers + '\n')
    return file_path

# Appends a line into a file by adding also the columns: [architecture, test_number]
def write_entry(line, new_file, architecture, test_number):
    with open(new_file, "a") as f:
        f.write(architecture + "," + test_number + "," + line + "\n")

# Parses a csv file
def csv_parser(architecture, test_number, original_file, parsed_file, chunk_dimension):
    global EXTENSION

    header_row = ""
    chunk_number = 1
    original_file = original_file + EXTENSION

    # Read the original file
    with open(original_file) as f:
        line_number = 0
        rows_in_parsed_file = 0
        for line in f:
            # Condition on first row (headers)
            if line_number == 0:
                # Write the header row onto a new file 
                header_row = "architecture,testNumber," + line
                chunk_file = parsed_file + "_chunk_" + str(chunk_number) + EXTENSION
                print("\tCreating chunk file: " + chunk_file)
                new_file = write_headers_file(chunk_file, header_row)
                line_number += 1
                continue
            # Condition on chunk_dimension:
            # If the new file is as big as wanted in term of rows (rows_in_parsed_file)
            if rows_in_parsed_file > 0 and rows_in_parsed_file % chunk_dimension == 0:
                chunk_number += 1
                rows_in_parsed_file = 0
                # Write the header row onto a new file
                chunk_file = parsed_file + "_chunk_" + str(chunk_number) + EXTENSION
                print("\tCreating chunk file: " + chunk_file)
                new_file = write_headers_file(chunk_file, header_row)
            # Write the row onto the pre-created file
            write_entry(line, new_file, architecture, test_number)
            # Increase rows_in_parsed_file
            rows_in_parsed_file += 1

def main():

    # Print docs if num args is not valid
    if not len(sys.argv) != 2:
        print (__doc__)
        sys.exit(1)

    # Config
    global EXTENSION
    global TEST_FOLDER
    global NEW_DIRECTORY
    global FILES_TO_PARSE
    
    architecture = sys.argv[1] # cloud vs on-premise
    chunk_dimension = int(sys.argv[2]) # es. 2000 means each file has 2000 records

    list_tests_folders = os.listdir(TEST_FOLDER + "/" + architecture)
    list_tests_folders.sort()
    list_tests_folders = [folder for folder in list_tests_folders if folder.startswith("test")]
    print("The following folders will be analized: " + str(list_tests_folders))

    # For each test
    for test_number in list_tests_folders:
        # For each file to parse
        for file_to_parse in FILES_TO_PARSE:

            # e.g. tests/on-premise/test1/aggregate_report (.csv extension will be added later)
            original_file = TEST_FOLDER + "/" + architecture + "/" + test_number + "/results/" + file_to_parse # No EXTENSION needed
            # e.g. tests/on-premise/test1/parsed/
            new_folder = TEST_FOLDER + "/" + architecture + "/" + test_number + "/" + NEW_DIRECTORY
            # e.g. tests/on-premise/test1/parsed/aggregate_report (.csv extension will be added later)
            new_file =  new_folder + "/" + file_to_parse

            print("Creating new folder: " + new_folder)
            create_folder(new_folder)

            print("Parsing: " + original_file + EXTENSION + " -> " + new_file + EXTENSION)
            csv_parser(architecture, test_number, original_file, new_file, chunk_dimension)

if __name__ == '__main__':
    main()
