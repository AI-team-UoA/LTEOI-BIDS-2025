# From Earth Observation Data to the Triple Store

## Part 2: Storing and Querying RDF Data with GraphDB

For this part of the tutorial you need to download and setup Docker

- Update apt and install prerequisites

        sudo apt-get update
        sudo apt-get install -y \
            ca-certificates \
            curl \
            gnupg \
            lsb-release

- Add Docker’s official GPG key

        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
            sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

- Set up the stable repository

        echo \
            "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
            https://download.docker.com/linux/ubuntu \
            $(lsb_release -cs) stable" | \
            sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

- Install Docker engine

        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

For Windows intsallations you can follow this [guide](https://docs.docker.com/desktop/setup/install/windows-install/). For this tutorial we suggest to follow the WSL instalation section of the guide.

### 1) Loading our RDF data into the GraphDB triple store

1. Create a directory name data/

        mkdir data
    
2. Transfer the knowledge graph datafiles inside the new directory:

        mv ../part1/output/*.nt data/

3. To build the docker image run:

        docker build -t graphdb .

4. To run the docker container image run:

        sudo docker run --name graphdb-container -p 7200:7200 graphdb

5. A GraphDB instance will be online on http://localhost:7200 with our knowledge graph loaded and ready to be queried!


### 2) Querying our RDF graph through SPARQL

SPARQL is a query language used to search and retrieve data from RDF (Resource Description Framework) graphs. It works a bit like SQL, but instead of querying tables, it looks for patterns in RDF data (subjects, predicates, objects). With SPARQL, you can ask questions like “find all people who live in Paris” or “list all resources of type Book” from RDF datasets.

2.1 Get 100 triples

```sparql
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix geo: <http://www.opengis.net/ont/geosparql#>
prefix schema: <http://schema.org/>
prefix onto: <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/>
prefix resource: <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resrouce/>

select * where {
    ?s ?p ?o .
} limit 100
```

2.2 Get 100 geometries

```sparql
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix geo: <http://www.opengis.net/ont/geosparql#>
prefix schema: <http://schema.org/>
prefix onto: <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/>
prefix resource: <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resrouce/>

select ?wkt where {
    ?s geo:hasGeometry ?g .
    ?g geo:asWKT ?wkt
} limit 100
```

2.3 Find Sentinel-2 images that contain points of interest

```sparql
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix geo: <http://www.opengis.net/ont/geosparql#>
prefix geof: <http://www.opengis.net/def/function/geosparql/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix schema: <http://schema.org/>
prefix onto: <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/>
prefix resource: <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resrouce/>

select distinct ?s2 where {
    ?s2 rdf:type onto:sentinel2 .
    ?s2 geo:hasGeometry ?g2 .
    ?g2 geo:asWKT ?wkt2 .
    
    ?poi rdf:type onto:poi .
    ?poi geo:hasGeometry ?g_poi .
    ?g_poi geo:asWKT ?wkt_poi .
    
    FILTER(geof:sfWithin(?wkt_poi,?wkt2))
} limit 100
```

2.4 Find all Sentinel-1 images that intersect with rivers and points of interest

```sparql
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix geo: <http://www.opengis.net/ont/geosparql#>
prefix geof: <http://www.opengis.net/def/function/geosparql/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix schema: <http://schema.org/>
prefix onto: <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/ontology/>
prefix resource: <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resrouce/>

select distinct ?s1 where {
    ?s1 rdf:type onto:sentinel1 .
    ?s1 geo:hasGeometry ?g1 .
    ?g1 geo:asWKT ?wkt1 .
    
    ?s_poi rdf:type onto:poi .
    ?s_poi geo:hasGeometry ?g_poi .
    ?g_poi geo:asWKT ?wkt_poi .
    
    ?river rdf:type onto:river .
    ?river geo:hasGeometry ?g_river .
    ?g_river geo:asWKT ?wkt_river .
    
    FILTER(geof:sfIntersects(?wkt_poi, ?wkt1) && geof:sfIntersects(?wkt_river, ?wkt1))
}

```
