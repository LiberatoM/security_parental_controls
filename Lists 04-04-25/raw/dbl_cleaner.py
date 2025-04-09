def clean_dot_prefix(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line.startswith('.'):
                line = line[1:]
            outfile.write(line + '\n')

def main():
    input_file = 'dbl.txt'   # Change this to your actual input file
    output_file = 'dbl_clean.txt' # Change this to your desired output file
    clean_dot_prefix(input_file, output_file)
    print(f"Clean file written to: {output_file}")

if __name__ == '__main__':
    main()
