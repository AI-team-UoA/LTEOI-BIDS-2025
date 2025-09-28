import csv
import sys

if len(sys.argv) != 3:
    print("Usage: python script.py <input_tsv> <output_csv>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

csv.field_size_limit(sys.maxsize)

# Open the input TSV file for reading
with open(input_file, 'r', newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    rows = list(reader)

# Open the output CSV file for writing
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)
