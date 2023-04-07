# Parse WinGet List to CSV

## Description

This program takes the standard command line output of `winget list` and converts it to a more usable `.csv` format.

The `parse.py` script reads the contents of an `input.txt` file, parses each line based on specific character indexes, and writes the extracted data into a new CSV file. The script takes two command-line arguments: the *input filename* and the *output filename*. If the output file already exists, the program creates a backup copy of it with a timestamp appended to the filename. The program also generates a console output with the progress and results of the parsing operation.

## Dependencies

This program is only designed for use with **Windows**.

This script requires the `csv`, `os`, `shutil`, `datetime`, and `argparse` modules. These modules are typically included in a standard `Python3` installation.

## How it works

The script parses each line in the input file by splitting its contents based on specific character indices within the line. The stripped contents are assigned to their respective variables and written to the output CSV file. If the output file already exists, a backup is created with a timestamp appended to its name.

First, save `parse.py` anywhere on your computer.

While in that directory, you need to generate a list of currently installed programs to import.

Execute the following command using command prompt:

```batch
winget list > input_file.txt
```

This will run `winget list` and pipe the output to a `input_file.txt` file.

Remove any unnecessary lines from the file so that **lines 1 and 2** lines are:

```
Name    Id    Version    Available Source
-----------------------------------------
```

Now that the input file is ready, make sure it is in the same directory as `parse.py`

`parse.py` takes an **input** text file and parses its contents into a CSV format with five columns:

- "Name"
- "Id"
- "Version"
- "Available"
- "Source"

The **output** CSV file is saved with the specified name in the arguments.

To run the script using Python, execute the following command using command prompt:

```batch
python parse.py "input_file.txt" "output.csv"
```

Where `"input_file.txt"` is the name of the file to be parsed and `"output.csv"` is the name of the output CSV file.