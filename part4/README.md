<div align="center">
  <h1>Visualization of results (Part 4)</h1>
</div>

In this part of our tutorial we will demonstrate a very simple web page that uses Pythia to retrieve satellite images and Leaflet.js  to draw their polygons on a map.

Leaflet.js is a straightforward mapping/visualization library that also manages to maintain high performance. In our experience it is a very good fit for creating maps with layers. In our usecase we use layers to overlay the polygons of our retrieved images.

## Pythia Server

Before we open our web page we must start the Pythia API server like so:

```sh
> python pythia.py server CUSTOM {kg-index-name}
```

This opens a server on port `1699` with the network interface `0.0.0.0`. You can change these default via the `--host` and `--port` command line arguments.

##### Remember all Pythia commands indlue `--help` functionality

Our server provides two APIs that we will be used by our web page:

- `/ask` is similar to our CLI in part 3, answering natural language requests over our knowledge graph.
- `/wkt` takes as input a sentinel image URI and returns its WKT. This is similar to the way that TerraQ's webapp handles visualization, so we copied the API for the purposes of this tutorial.

## Web Page

In the `webpages/` directory of this part you can find two `.html`. files. Each one of them is a simple very simple web page that uses Pythia's APIs to query the graph. You can open these on pretty much any web browser.

`no_map.html` is provided to familiarize the reader with the skeleton of this web application. It contains an input where a question is written, a button to send a request to the `/ask` API endpoint, and finally some simple parsing and textual visualization logic.

Once the reader is familiar with this file they can move on to `complete.html` where the differences that enable mapping visualization are highlighted and explained.

#### Leaflet CSS

Any page that uses Leaflet must include its CSS sheet:

```html
link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
  crossorigin=""/>
``` 

#### Creating a container for Leaflet

To function, Leaflet requires a container tagged `map` and a set `height` property.

```html
<div id="map" style="height: 500px; width: 100%; margin-top: 16px;"></div>
```

#### Scripting

We import the following scripts:

```html
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script src="https://unpkg.com/wellknown/wellknown.js"></script>
```

We initialize our map:

```js
const map = L.map(mapDiv).setView([53.5511, 9.9937], 6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19
}).addTo(map);
```

We create a function to interact with `/wkt`:

```js
async function getWKT(uri){
  const res = await fetch('http://localhost:1699/wkt', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ uri })
  });
  const j = await res.json();
  return j.wkt;
}
```

And finally our main logic for clearing and adding layers to our map:

```js
// Clear map
map.eachLayer(layer => {
  if(layer instanceof L.Polygon || layer instanceof L.Marker) map.removeLayer(layer);
});

// For each entry other than first (CSV header)
for(let i=1; i<resultData.length; i++){
  const [uri, wkt] = resultData[i];
  let geometry = wkt;

  if(!geometry){
    geometry = await getWKT(uri);
  }

  if(geometry){
    const geojson = wellknown.parse(geometry);
    if(geojson){
      const layer = L.geoJSON(geojson).addTo(map);
      map.fitBounds(layer.getBounds());
    }
  }
}
```
