# Plumbing and internals

For those who want to understand how the plugin works, here is a brief overview.

## Diagrams.net

**Diagrams.net** previoully known as **Draw.io** is a free online diagram software. It is perfect for creating diagrams, flowcharts, process diagrams, and more. It is a powerful tool that can be used for creating diagrams for any purpose.

It relies on JTGraph's [mxGraph](https://jgraph.github.io/mxgraph/) library to render the diagrams. A mxGraph is a XML-based language that defines the structure of the diagram. Here an example

![](circle-square.drawio)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" version="26.0.7">
  <diagram name="Page-1" id="mV4jbraemd7C51ydpzk2">
    <mxGraphModel dx="565" dy="355" grid="1" gridSize="10"
        guides="1" tooltips="1" connect="1" arrows="1" fold="1"
        page="1" pageScale="1" pageWidth="394" pageHeight="394"
        math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="7JHgTfKEjFP575Ptm9la-1" value=""
            style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;"
            vertex="1" parent="1">
          <mxGeometry x="80" y="40" width="80" height="80" as="geometry" />
        </mxCell>
        <mxCell id="7JHgTfKEjFP575Ptm9la-2" value=""
            style="whiteSpace=wrap;html=1;aspect=fixed;
                   fillColor=#f8cecc;strokeColor=#b85450;"
            vertex="1" parent="1">
          <mxGeometry x="180" y="40" width="80" height="80" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## GraphViewer

The plugin uses the [GraphViewer](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/js/viewer-static.min.js) minified version of the drawio viewer.

This is a standalone viewer for drawio diagrams that can be embedded in any web page to convert mxGraph XML to SVG. It features a lightbox mode and a toolbar with buttons to zoom, edit, and navigate the diagram.

## The Plugin

This plugin heavily relies on the GraphViewer to render the diagrams. The MkDocs plugin is responsible for passing configuration options to the viewer and ensure compatibility across MkDocs themes.

Furthermore, it provides a way to extract pages from diagrams to only serve the necessary content to the user. This is useful when you have a large diagram and only want to show a specific part of it.
