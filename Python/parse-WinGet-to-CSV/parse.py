import csv
import os
import shutil
import datetime
import argparse

# Execute this file with command prompt: python parse.py "input_file.txt" "output.csv"

#
# This method parses the input parameters into an object.
# If it encounters an error during the process the program will exit.
# 
# @return An object containing the input parameters
#
def checkArgs():
    # Create argument parser to get input and output filenames from command-line
    parser = argparse.ArgumentParser(
        description='Parse file contents into CSV format')
    parser.add_argument('input', metavar='input_filename',
                        type=str, help='input filename')
    parser.add_argument('output', metavar='output_filename',
                        type=str, help='output filename')
    try:
        args = parser.parse_args()
        return args
    except:
        print("Error! Invalid arguments")
        exit()

#
# This method parses the provided input file by splitting the
# contents of each line based on char index within the line.
# It then strips the remaining contents and assigns it to a variable.
# Finally, the line is written to the csv file. Once the loop finishes
# the file is saved and the program is exited.
# 
def parse():
    # Check args before proceeding
    args = checkArgs()

    # Set input/output filenames to arguments
    input_filename = args.input
    output_filename = args.output

    # Check if output file already exists
    if os.path.isfile(output_filename):
        # Append timestamp to filename for backup
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_filename = f'output_{timestamp}.csv'
        shutil.copyfile(output_filename, backup_filename)
        print(f'Backup created: {backup_filename}')

    with open(input_filename, 'r') as f, open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Name', 'Id', 'Version', 'Available', 'Source'])
        lineIndex = 1

        for line in f:
            if 'Name' not in line and '---' not in line and line.strip():
                lineIndex = lineIndex + 1
                name = line[0:41].strip()
                id = line[41:82].strip()
                version = line[82:103].strip()
                available = line[103:113].strip()
                source = line[113:].strip()
                csvwriter.writerow([name, id, version, available, source])
                print(
                    f"Row {lineIndex:<5} Name: {name:<50} Id: {id:<50} Version: {version:<25} Available: {available:<25} Source: {source:<10}")


if __name__ == "__main__":
    parse()
