import os
import random
import csv
import sys

# Program to extract a number of random lines from a txt or csv file
# Usage python3 random_lines.py file num_lines

def pick_random_lines(file_path, num_lines):
    # Get the file extension
    file_name, file_extension = os.path.splitext(file_path)

    # Prepare output file name
    output_file = f"{file_name}_random_lines{num_lines}{file_extension}"

    # Handle CSV or TXT files
    if file_extension.lower() == '.csv':
        random_lines_from_csv(file_path, num_lines, output_file)
    elif file_extension.lower() == '.txt':
        random_lines_from_text(file_path, num_lines, output_file)
    else:
        print(f"Unsupported file type: {file_extension}")

def random_lines_from_text(file_path, num_lines, output_file):
    try:
        # Open file with utf-8 encoding to avoid UnicodeDecodeError
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Select random lines without repetition
        random_lines = random.sample(lines, min(num_lines, len(lines)))

        # Write choseh lines to the new file
        with open(output_file, 'w', encoding='utf-8') as file:
            for i, line in enumerate(random_lines):
                if i < len(random_lines) - 1:
                    file.write(line)
                else:
                    file.write(line.rstrip('\n'))  # Remove extra newline from the last line

        print(f"{num_lines} random lines saved to {output_file}")
    except UnicodeDecodeError:
        print(f"Error: Unable to read the file due to encoding issues.")
    except ValueError:
        print(f"Error: Not enough lines to pick {num_lines} random lines.")

def random_lines_from_csv(file_path, num_lines, output_file):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            lines = [row[1] for row in reader if len(row) > 1]  # Extract the second column

        # Select random lines avoiding repetition
        random_lines = random.sample(lines, min(num_lines, len(lines)))

        # Write chosen lines to the new file with no extra newline at the end
        with open(output_file, 'w', encoding='utf-8') as file:
            for i, line in enumerate(random_lines):
                if i < len(random_lines) - 1:
                    file.write(line + '\n')
                else:
                    file.write(line)  # No extra newline for the last line

        print(f"{num_lines} random lines from column B saved to {output_file}")
    except UnicodeDecodeError:
        print(f"Error: Unable to read the CSV file due to encoding issues.")
    except ValueError:
        print(f"Error: Not enough lines to pick {num_lines} random lines.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 random_lines.py file num_lines")
    else:
        file_path = sys.argv[1]
        num_lines = int(sys.argv[2])
        pick_random_lines(file_path, num_lines)
