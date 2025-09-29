# From Earth Observation Data to the Triple Store

## Part 1: From Unstructured EO Data to RDF with Python

In this part of the tutorial we will be transforming files containing geospatial information about the city of [Hamburg](https://en.wikipedia.org/wiki/Hamburg) alongside Sentinel-1 and Sentinel-2 satellite data, into RDF data. The input files can be found under the directory geojsons/ and are in [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) form, an extension of JSON to model geospatial information in a semi-structured format. The derised output of this part of the tutorial is RDF data in NTriples form.

For this part of the tutorial you need to install the following package:

        pip install toposkg

To have access to the toposkg library and it's RDF parsing capabilities

### 1) Parsing GeoJSON Naively

The parsing library of toposkg allows the user to parse a wide array of semi-structured data (CSV,JSON,XML,KML,GeoJSON, etc.) and transofrm them into RDF data. One of the two approaches the library uses in the naive converter classes. These classes take as input a semi-structured data source and provide a simple represntation of the data source into RDF data. To achieve this we will built a simple python script

1.1 Create a directory called output/

    mkdir output

1.2 Import the libraries

```python
from toposkg.converter.toposkg_lib_geojson_converter import GeoJSONConverter
import os
```

1.3 Select URIs for our ontology

RDF data and knowledge graphs operate on interent resources. A URI is a string that identifies a resource, while a URL is a type of URI that also tells you how and where to access that resource on the web. An example of a URI from wikidata for Hamburg is:

    <https://www.wikidata.org/wiki/Q1055>

For our part, we will base our URIs, on the tutorial site's URL. Keep in mind that the RDF data we will generate are not actual URIs and accessing them through a browser will result to nothing:

```python
#Ontology URIs for classes and properties (ontology_uri) and resources (resource_uri)
ontology_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/"
resource_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resource/"
```

1.4 Iterate through our GeoJSON data in the directory geojsons/

```python
#Helper function to change the extension of a file
output_dir = "./output/"
def change_to_nt(file_path, ext):
    base, _ = os.path.splitext(os.path.basename(file_path))  # keep only the filename
    return os.path.join(output_dir, base + f".{ext}")

# Iterate throught the directory with the json files
directory_in_str = "./geojsons/"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    #The path to one of the geojson files e.g. /geojsons/hamburg.geojson
    geojson_file = os.path.join(directory_in_str, filename)
    #A string for our output file
    output_nt_file = change_to_nt(geojson_file,"nt")
```

1.5 Inside the loop create the converter class for each file to generate an RDF output

```python
    #Create the converter for GeoJSON files
    converter = GeoJSONConverter(geojson_file,output_nt_file,ontology_uri,resource_uri)
    #Parse the input file
    converter.parse()
    #Export to the output file
    converter.export()
```

The comlpete script is shown bellow:

```python
from toposkg.converter.toposkg_lib_geojson_converter import GeoJSONConverter
import os

#Ontology URIs for classes and properties (ontology_uri) and resources (resource_uri)
ontology_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/"
resource_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resource/"

def change_to_nt(file_path, ext):
    base, _ = os.path.splitext(file_path)
    return base + ".{}".format(ext)

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

```

This script will generate a .nt (NTriples) file for each input .geojson file in the directory. These output files are valid RDF data that can be loaded and queried into an RDF store. You can browse the generated files in the output/ directory after you run the script


### 2) Parsing GeoJSON files using RML mappings

The previous method is simple, but it does not let you change how the RDF data looks. In many cases, when creating RDF data, we need more control over the ontology and how it works. To do this, we can use RML mappings, which allow us to build a more flexible RDF graph. RML (RDF Mapping Language) is a way to turn data from different formats (like CSV, JSON, or databases) into RDF, so the data can be linked and shared on the web.

The Toposkg library includes a default mapping generator. This tool creates a basic RML mapping file for your input data. You can then edit this file to fit your needs, and by running it through an RML processor, the library will generate RDF data based on your customized mapping.

2.1 Import the libraries

```python
from toposkg.converter.rml.toposkg_lib_default_mapping_generator import DefaultMappingGenerator
import os
```

2.2 Select URIs for our ontology

```python
#Ontology URIs for classes and properties (ontology_uri) and resources (resource_uri)
ontology_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/"
resource_uri = "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resource/"
```

2.3 Create a default mapping generator object

```python
#Create a default mapping generator object
generator = DefaultMappingGenerator()
```

2.4 Iterate through geojsons/ dir and create a mapping for each geojson file

```python
#Helper function to change the extension of a file
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
    output_mapping_file = change_to_nt(geojson_file,"ttl")
```

2.5 Inside the loop call the generate_mappings() method to create a .ttl file containing the default mappings for each file

```python
generator.generate_mappings("GeoJSON", geojson_file, output_mapping_file)
```

Our script so far:
```python

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
generator = DefaultMappingGenerator()

# Iterate throught the directory with the json files
directory_in_str = "./geojsons/"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    geojson_file = os.path.join(directory_in_str, filename)
    output_mapping_file = change_to_nt(geojson_file,"ttl")
    generator.generate_mappings("GeoJSON", geojson_file, output_mapping_file)
```

2.6 If we go the directory output/ we can see all the mappings generated for each file. We can now edit this files to create more customizable mappings. For example we can explicitly say to the RML processor to add a triple that indicates the class of each entity. For example for the POIs in Hamburg, presented im the file /geojsons/hamburg_poi.geojson we can edit the following mapping:

    <#FeatureMap>  a rr:TriplesMap;
    rml:logicalSource [
            rml:source "./geojsons/_7ee82c0188668588a605614621fc3804hamburg_poi.geojson";
            rml:iterator "$.features[*]";
            rml:referenceFormulation ql:JSONPath;
    ];
    rr:subjectMap [
        rr:template "https://example.org/resource/{_pyrml_mapper_generated_id}";
    ];

Which is responsible for create an entity for each POI present in the geojson file, to the following:

    <#FeatureMap>  a rr:TriplesMap;
    rml:logicalSource [
            rml:source "./geojsons/_7ee82c0188668588a605614621fc3804hamburg_poi.geojson";
            rml:iterator "$.features[*]";
            rml:referenceFormulation ql:JSONPath;
    ];
    rr:subjectMap [
        rr:template "https://example.org/resource/{_pyrml_mapper_generated_id}";
        rr:class onto:poi  <-- Add POI class here
    ];

Adding these classes explicitly is very important for the next parts of the tutorial, as it makes it easier for the question answering engine to locate entities through their types. We can do that for each class and for each mapping.

2.7 After editing the files to our liking, we can finally generate the RDF triples, by calling the method generate_triples()

```python
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
generator = DefaultMappingGenerator()

# Iterate throught the directory with the json files
directory_in_str = "./geojsons/"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    geojson_file = os.path.join(directory_in_str, filename)
    output_mapping_file = change_to_nt(geojson_file,"ttl")
    output_nt_file = change_to_nt(geojson_file,"nt")
    generator.generate_triples(output_mapping_file, output_nt_file) #We call the generate_triples() method for each mapping
```
The generated output RDF files are available in the output/ directory. All the scripts are present inside the current directory and can be run directly to produce the desired results:

- geojson_to_ntriples_naive.py: Naive method
- geojson_to_mapping.py: RML method to generate mappings
- mapping_to_triples.py: Mappings to RDF data generator







