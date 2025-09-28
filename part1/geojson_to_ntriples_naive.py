from toposkg.converter.toposkg_lib_geojson_converter import GeoJSONConverter
import os

#Ontology URIs for classes and properties (ontology_uri) and resources (resource_uri)
ontology_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/"
resource_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resource/"

output_dir = "./output/"
def change_to_nt(file_path, ext):
    base, _ = os.path.splitext(os.path.basename(file_path))  # keep only the filename
    return os.path.join(output_dir, base + f".{ext}")

# Iterate throught the directory with the json files
directory_in_str = "./geojsons/"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    geojson_file = os.path.join(directory_in_str, filename)
    output_nt_file = change_to_nt(geojson_file,"nt")
    #Create the converter for GeoJSON files
    converter = GeoJSONConverter(geojson_file,output_nt_file,ontology_uri,resource_uri)
    #Parse the input file
    converter.parse()
    #Export to the output file
    converter.export()
