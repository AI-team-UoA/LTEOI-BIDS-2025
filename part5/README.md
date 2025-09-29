# Optimizing for realtime performance

## Part 5: Query execution optimization with JedAI-Spatial and GoST

To proceed on this part of the tutorial Java 8 needs to installed.

### 1) Usings JedAI-Spatial to optimize geospatial query execution

Geospatial queries are often very computationally expensive. To mitigate that cost, we use JedAI-Spatial to pre-calculate and materialize expensive operations like within, intersects, covers, etc. For this part of the tutorial, the .jar binaries are provided in this directory.

1.1 Concatenate all .nt files in two files, one for satelites and one for the rest of the data:

        cat ../part1/output/hamburg_s*.nt > bids2025_s.nt
        cat ../part1/output/hamburg.nt ../part1/output/hamburg_poi.nt ../part1/output/hamburg_river.nt > bids2025_rest.nt

1.2 Run jedai_spatial_pipeline.sh to create .csv files for ready for the materialization process:

        ./jedai_spatial_pipeline.sh bids2025_s.nt
        ./jedai_spatial_pipeline.sh bids2025_rest.nt

1.3 Create a file to save the results of the materialization

        touch bids2025_mat.nt

1.4 Run JedAI-Spatial and follow the CLI instructions. Since we want to discover relationships between satelites and the rest of the geospatial entites our source will be bids2025_rest_no_crs_geo_only.csv and target will be bids2025_s_no_crs_geo_only.csv

        java -cp geospatialinterlinking-1.0-SNAPSHOT-jar-with-dependencies.jar workflowManager.CommandLineInterface cli

1.5 The materialized pairs are now stored in the file bids2025_mat.nt in an intermediate state. To complete the mapping run the following command:

        ./jedai_map.sh bids2025_mat.nt bids2025_rest_no_crs_geo_only.tsv bids2025_s_no_crs_geo_only.tsv

1.6 The final materialized relationships are stored in the file bids2025_mat_map.nt. We can store in this file in our database through GraphDB's UI.

### 2) Usings GoST to rewrite queries

After our materialization process is finished and the new triples are stored in the database, we can use these newly generated RDF data to preform faster queries. To utilize them however, we first have to transform GeoSPARQl queries using spatial functions like geo:sfWithin() or geo:sfIntersects to simple SPARQL queries that utilize the new materialized triples. We can do that through GoST

2.1 Run a query through GoST, to rewrite it so it utilizes the materiliazed relationships:

        java -cp GoST-1.0-SNAPSHOT.jar gr.uoa.di.ai.gost.Transpiler "prefix xsd: <http://www.w3.org/2001/XMLSchema#>prefix geo: <http://www.opengis.net/ont/geosparql#>prefix geof: <http://www.opengis.net/def/function/geosparql/>prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>prefix schema: <http://schema.org/>prefix onto: <https://example.org/ontology/>prefix resource: <https://ai-team-uoa.github.io/LTEOI-BIDS-2025/resrouce/>select distinct ?s1 where {    ?s1 rdf:type onto:sentinel1 .    ?s1 geo:hasGeometry ?g1 .    ?g1 geo:asWKT ?wkt1 .        ?s_poi rdf:type onto:poi .    ?s_poi geo:hasGeometry ?g_poi .    ?g_poi geo:asWKT ?wkt_poi .        ?river rdf:type onto:river .    ?river geo:hasGeometry ?g_river .    ?g_river geo:asWKT ?wkt_river .        FILTER(geof:sfIntersects(?wkt_poi, ?wkt1) && geof:sfIntersects(?wkt_river,?wkt1))}"


2.2 Run the generated query in GraphDB. Notice any difference in the execution speed?
