################################
# Dockerfile for DA4DTE's KG   #
# DI @ UoA                     #
#                              #
# Java 11                      #
# graphdb 10.6.3               #
################################

FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

ENV PORT 7200
ENV GRAPH_DB_VERSION 10.6.3

# INSTALL PREREQUISITIES
RUN apt-get update \
 && apt-get install -y \
    wget \
    openjdk-11-jdk \
    curl \
    unzip \
    gzip \
    gnupg2 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Download and extract graphdb
RUN wget "https://maven.ontotext.com/repository/owlim-releases/com/ontotext/graphdb/graphdb/${GRAPH_DB_VERSION}/graphdb-${GRAPH_DB_VERSION}-dist.zip" \
	&& unzip graphdb-${GRAPH_DB_VERSION}-dist.zip

# Copy the knowledge graph data
COPY data/* .

# Extract the knowledge graph data

COPY template.ttl . 

EXPOSE 7200
EXPOSE 7300

RUN ./graphdb-10.6.3/bin/importrdf preload -c template.ttl *.nt
ENTRYPOINT ["./graphdb-10.6.3/bin/graphdb"]
