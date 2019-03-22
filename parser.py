#!/usr/bin/env python

"""
USAGE:

$ parser.py cloud 1000
$ parser.py on-premise 2000
"""

import os
import re
import sys
import csv
from urllib.parse import urlparse, parse_qs

extension = ".csv"
test_folder = "tests"
NEW_DIRECTORY = "parsed"

files_to_extract = [
    'aggregate_report'
]

def create_folder(directory): 
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_headers_file(file_path, headers):
    with open(file_path, "w") as f:
        f.write(headers + '\n')
    return file_path

def write_entry(line, new_file, architecture, test_number):
    with open(new_file, "a") as f:
        f.write(architecture + "," + test_number + "," + line + "\n")

def csv_parser(architecture, test_number, original_file, parsed_file, chuch_dimension):
    global extension
    header_row = ""
    chunch_number = 1

    original_file = original_file + extension

    with open(original_file) as f:
        line_number = 0
        line_in_parsed_file = 0
        for line in f:
            # Avoid to parse headers
            if line_number == 0:
                header_row = "architecture,testNumber," + line
                chunch_file = parsed_file + "_chunch_" + str(chunch_number) + extension
                print("\tCreating chunch file: " + chunch_file)
                new_file = write_headers_file(chunch_file, header_row)
                line_number += 1
                continue
            # End chunch file
            if line_in_parsed_file > 0 and line_in_parsed_file % chuch_dimension == 0:
                chunch_number += 1
                line_in_parsed_file = 0
                chunch_file = parsed_file + "_chunch_" + str(chunch_number) + extension
                print("\tCreating chunch file: " + chunch_file)
                new_file = write_headers_file(chunch_file, header_row)
            write_entry(line, new_file, architecture, test_number)
            # Increase line_in_parsed_file
            line_in_parsed_file += 1

def main():
    if not len(sys.argv) != 2:
        print (__doc__)
        sys.exit(1)
    global extension
    global test_folder
    global files
    global parsed_folder
    outputFiles = {}
    architecture = sys.argv[1] # cloud vs on-premise
    chuch_dimension = int(sys.argv[2]) # es. 2000 means each file has 2000 records
    list_tests_folders = os.listdir(test_folder + "/" + architecture)
    list_tests_folders.sort()
    list_tests_folders = [folder for folder in list_tests_folders if folder.startswith("test")]
    print(list_tests_folders)

    for test_number in list_tests_folders:
        for file_to_extract in files_to_extract:

            # e.g. tests/on-premise/test1/aggregate_report.csv
            original_file = test_folder + "/" + architecture + "/" + test_number + "/results/" + file_to_extract
            # e.g. tests/on-premise/test1/parsed/aggregate_report.csv
            new_folder = test_folder + "/" + architecture + "/" + test_number + "/" + NEW_DIRECTORY
            parsed_file =  new_folder + "/" + file_to_extract # No extension needed

            print("Creating new folder: " + new_folder)
            create_folder(new_folder)

            print("Parsing: " + original_file + extension + " -> " + parsed_file + extension)
            csv_parser(architecture, test_number, original_file, parsed_file, chuch_dimension)

if __name__ == '__main__':
    main()
