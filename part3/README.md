<div align="center">
  <h1>Pulling down the SPARQL barrier for RDF access (Part 3)</h1>
</div>

Now that our RDF knowledge graph is ready to be queried, we will make it more accessible by providing a **natural language interface** powered by [Pythia](https://github.com/SKefalidis/Pythia).

Pythia is a knowledge graph-agnostic **question-answering** engine that translated natural languge into SPARQL/GeoSPARQL/stSPARQL queries. This way it makes knowledge graphs easier to use by humans and accessible by AI agents. As all of our group's software and data, Pythia is open-source and can be used by anyone free of charge.

## Preliminaries

### Download Pythia

This tutorial was designed with version v0.1-pre1 of Pythia in mind. You can find this version in the official [repository](https://github.com/SKefalidis/Pythia).

Download Pythia either via the web interface or via git:

```sh
> git clone https://github.com/SKefalidis/Pythia.git
```

### Dependencies

Dependencies are handled via Conda. The environment file `pythia-3.10-environment.yml` contains all required dependencies. You can use it like so:

```sh
> conda env create -f pythia-3.10-environment.yml
```

This will create a *Conda* environment which can be activated like so:

```sh
> conda activate pythia
```

### pythia.py

If you haven't not yet entered the root directory do so with this command:

```sh
> cd Pythia
```

At this point Pythia can be accessed through its unified interface script (`pythia.py`) that resides in its root directory.

Let's make sure that everything is in order:

```sh
> python pythia.py --version
```

If this command prints the version and copyright information of the software you are ready to move forward!

### Compiling Java helpers

Before we proceed with using Pythia we first need to compile a Java helper program (if we forget this step Pythia will remind use!).

To do so we need to have Java installed and run the following command:

```sh
> cd tools/kg_entity_extractor && mvn package
```

## Using Pythia on our Knowledge Graph

### Preparing Pythia to query our Knowledge Graph

##### KG_DIR is a directory where the source RDF files of our knowledge graph reside.

Before Pythia is ready to answer our questions we must let it "learn" our knowledge graph. To do so we use the `index` command. This creates a number of indices that are used by Pythia to query our knowledge graph.

`index` has a lot of options which can be used by advanced users to create specific indices to help Pythia perform better. In this tutorial we will limit ourselves to (mostly) the default configuration.

The three options that we will employ are:
- `--labels` is used to let Pythia know how to reach the name/label of each non-class node in our knowledge graph. This is very helpful for named entity disambiguation and something that you should always do.
- `--filter` this option tells Pythia to discard from each indices any non-class nodes that don't have a label. In our case we have a bunch of intermediate nodes in our knowledge graph, which we don't want to utilize for named entity disambiguation.
- `-t` is an option that tells Pythia how many processing threads to use. Since your knowledge graph is small, we can use a single thread.

```sh
> python pythia.py index {kg-directory} --labels "https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/propertiesLink->https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/hasGADM_Name,https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/propertiesLink->https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/hasName" -t 1 --filter
```

After a bit Pythia will prompt you about whether the given knowledge graph contains non-descriptive URIs. Our knowledge graph contains such URIs, so we will answer positively.

```sh
Does your knowledge graphs contain URIs with non-descriptive IDs, e.g., /m.02mjmr, /Q42? (y/n)
> y
```

It will then prompt you to input predicates/predicate paths that provide descriptive labels to your URIs. We use the same predicate paths that we used for our labels (comma separated).

```sh
Please provide Pythia with one or more predicate URIs that can be used to fetch labels (e.g. http://www.w3.org/2000/01/rdf-schema#label).

If multiple, separate them with commas. Press Enter when done:

> https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/propertiesLink->https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/hasGADM_Name,https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/propertiesLink->https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/hasName
```

After this is done, the last part of the indexing process is a question regarding geospatial data. Again, we do have geopsatial data in our knowledge graph, and luckily we use the standard OGC grammar to describe them so we don't need to change anything.

```sh
Does your knowledge graph contain geospatial data with WKT literals? (y/n)
> y

Please provide Pythia with one or more predicate URI chains (->) that can be used to fetch WKT literals (e.g. http://www.opengis.net/ont/geosparql#hasGeometry->http://www.opengis.net/ont/geosparql#asWKT).
If multiple, separate them with commas. Press Enter when done (default: http://www.opengis.net/ont/geosparql#hasGeometry->http://www.opengis.net/ont/geosparql#asWKT)

"Just press enter"
```

A new `indices/` folder has been created in our root directory, and inside it lies a folder with all the information that Pythia gathered during the indexing process.

### Configuration

We are almost ready to start writing queries with Pythia. To make our life easier and reduce the amount of arguments that we have to write we will proceed with editing the `config.yaml` file in the root directory.

This file contains configuration options for Pythia, like which RDF endpoint to use or which LLM inference provider. Most of these options can als obe passed as command line arguments to `pythia.py` but setting them here is usually simpler. 

For the purposes of this tutorial we only have to edit:
- `llm_api_key`: We will be using OpenAI models, so we need to provide an API key. A key will be provided during the demonstration. *Instructions for different providers/local models will be available after the conclusion of BiDS.*
- `endpoint_url`: Here we add the URL of the GraphDB endpoint that we created in the previous part.
- `endpoint_username` and `endpoint_password` if the endpoint is not public. If it is public we leave them empty.

Additionally, to align Pythia with our expectations for this tutorial, we want to pass it some additional instructions. These are given to its query generation component and allow us to easily modify the behavior of Pythia without editing its codebase.

The following command should open the default text editor of your operating system:
```sh
> python pythia.py configure custom-instruction
```

In the opened file write:
```
My knowledge graph contains satellite images.
Satellite images cover very large areas. 
When I say that I want an image of some place I want you to an "intersection" unless I specifically say otherwise.
For example "Images of Athens", give me images that intersect with Athens.
If I say "images that contain Athens" then show me images that fully contain Athens.
```

This text instructs Pythia to use `geof:sfIntersects` to express that an image contains something. In the case of satellite images this is a reasonable compromise between getting lots of images and accurate images.

### Queries

We are now ready to proceed with running Pythia for the first time:

```sh
python pythia.py cli CUSTOM {kg-index-name}
```

After Pythia has finished loading we can try asking it some questions in natural language. It will process them and attempt to generate semantically equivalent formal queries them based on the contents of our knowledge graph.

### Examples

#### Give me 5 sentinel-2 images.
```sparql
SELECT DISTINCT ?image WHERE {
  ?image <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/sentinel2> .
}
LIMIT 5
```

#### Give me 5 sentinel-2 images of Hamburg.
```sparql
SELECT DISTINCT ?sentinel2Image ?imageURL WHERE {
  <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resource/54d45ac715ef82eb94ea4bbf57b5211c_1> <http://www.opengis.net/ont/geosparql#hasGeometry> ?hamburgGeomNode .
  ?hamburgGeomNode <http://www.opengis.net/ont/geosparql#asWKT> ?hamburgWKT .
  
  ?sentinel2Image <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/sentinel2> .
  ?sentinel2Image <http://www.opengis.net/ont/geosparql#hasGeometry> ?imageGeomNode .
  ?imageGeomNode <http://www.opengis.net/ont/geosparql#asWKT> ?imageWKT .
  
  ?sentinel2Image <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/propertiesLink> ?propLink .
  ?propLink <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/derivedFrom> ?imageURL .
  
  FILTER(geof:sfIntersects(?imageWKT, ?hamburgWKT))
}
LIMIT 5
```

#### Give me 5 sentinel-2 images of Hamburg with less than 10% cloud coverage.
```sparql
SELECT DISTINCT ?image WHERE {
  BIND(<https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resource/54d45ac715ef82eb94ea4bbf57b5211c_1> AS ?hamburg)
  
  ?image a <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/sentinel2> .
  ?image <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/propertiesLink> ?props .
  ?props <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/hasMediumProbaCloudsPercentage> ?cloudCoverage .
  FILTER(?cloudCoverage < 10)
  
  ?hamburg <http://www.opengis.net/ont/geosparql#hasGeometry> ?hamburgGeo .
  ?hamburgGeo <http://www.opengis.net/ont/geosparql#asWKT> ?hamburgWKT .
  
  ?image <http://www.opengis.net/ont/geosparql#hasGeometry> ?imageGeo .
  ?imageGeo <http://www.opengis.net/ont/geosparql#asWKT> ?imageWKT .
  
  FILTER(geof:sfIntersects(?imageWKT, ?hamburgWKT))
}
LIMIT 5
```
