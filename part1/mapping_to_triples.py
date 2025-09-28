from toposkg.converter.rml.toposkg_lib_default_mapping_generator import DefaultMappingGenerator
import os

#Ontology URIs for classes and properties (ontology_uri) and resources (resource_uri)
ontology_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/"
resource_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resource/"

def change_to_nt(file_path, output_dir, ext):
    base, _ = os.path.splitext(os.path.basename(file_path))  # keep only the filename
    return os.path.join(output_dir, base + f".{ext}")

#Create a default mapping generator object
generator = DefaultMappingGenerator()

# Iterate throught the directory with the json files
directory_in_str = "./geojsons/"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    geojson_file = os.path.join(directory_in_str, filename)
    if not filename.startswith("_"):
        output_mapping_file = change_to_nt(geojson_file,"./mappings/","ttl")
        output_nt_file = change_to_nt(geojson_file,"./output/","nt")
        generator.generate_triples(output_mapping_file, output_nt_file) #We call the generate_triples() method for each mapping