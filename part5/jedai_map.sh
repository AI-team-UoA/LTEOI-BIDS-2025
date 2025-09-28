#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <nt_file> <tsv_source_file> <tsv_target_file>"
    exit 1
fi

nt_file="$1"
tsv_source_file="$2"
tsv_target_file="$3"

echo "Mapping discovered relationships to entities..."
java -cp DuplicateGeometryRemover-1.0-SNAPSHOT.jar DGR JedAISpatialMap "$nt_file" "$tsv_source_file" "$tsv_target_file"
