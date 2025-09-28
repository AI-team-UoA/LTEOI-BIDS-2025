from toposkg.converter.rml.toposkg_lib_default_mapping_generator import DefaultMappingGenerator
import os

#Ontology URIs for classes and properties (ontology_uri) and resources (resource_uri)
ontology_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/"
resource_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resource/"

output_dir = "./output/"
def change_to_nt(file_path, ext):
    base, _ = os.path.splitext(os.path.basename(file_path))  # keep only the filename
    return os.path.join(output_dir, base + f".{ext}")

#Create a default mapping generator object
generator = DefaultMappingGenerator(ontology_uri, resource_uri)

# Iterate throught the directory with the json files
directory_in_str = "./geojsons/"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    geojson_file = os.path.join(directory_in_str, filename)
    output_mapping_file = change_to_nt(geojson_file,"ttl")
    generator.generate_mappings("GeoJSON", geojson_file, output_mapping_file)

