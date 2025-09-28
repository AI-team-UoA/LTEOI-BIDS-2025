#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

input_file="$1"
base_name="${input_file%.*}"
extension="${input_file##*.}"

# Step 1: Run RemoveEPSGTag
no_crs_file="${base_name}_no_crs.${extension}"
echo "Running RemoveEPSGTag..."
java -cp DuplicateGeometryRemover-1.0-SNAPSHOT.jar DGR RemoveEPSGTag "$input_file"

# Step 2: Run NTriplesToTSV
geo_only_tsv="${base_name}_no_crs_geo_only.tsv"
echo "Running NTriplesToTSV..."
java -cp DuplicateGeometryRemover-1.0-SNAPSHOT.jar DGR NTriplesToTSV "$no_crs_file"

# Step 3: Convert TSV to CSV
output_csv="${base_name}_no_crs_geo_only.csv"
echo "Converting TSV to CSV..."
python3 cs.py "$geo_only_tsv" "$output_csv"

echo "Process completed. Output CSV: $output_csv"
