def remove_http_prefix(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line.startswith('http://'):
                line = line[len('http://'):]
            elif line.startswith('https://'):
                line = line[len('https://'):]
            outfile.write(line + '\n')

def main():
    input_file = 'url_abuse.txt'    # Replace with your actual input filename
    output_file = 'url_abuse_clean.txt'  # Replace with your desired output filename
    remove_http_prefix(input_file, output_file)
    print(f"Cleaned URLs written to: {output_file}")

if __name__ == '__main__':
    main()
