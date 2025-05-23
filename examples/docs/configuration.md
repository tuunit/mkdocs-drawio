# Configuration

## Diagram options

By default the plugin uses the official url for the minified drawio javascript library. To use a custom source for the drawio viewer you can overwritte the url. This might be useful in airlocked environments.

```yaml
plugins:
  - drawio:
      viewer_js: "https://viewer.diagrams.net/js/viewer-static.min.js"
```

Further options are the following with their default value:

```yaml
plugins:
  - drawio:

      # URL to the Drawio viewer JavaScript file
      viewer_js: "https://viewer.diagrams.net/js/viewer-static.min.js"

      # Enable tooltips on diagram elements
      tooltips: true

      # Border size / padding around diagrams
      border: 5

      # Enable opening the editor for diagrams
      edit: true

      # Enable dark mode support
      # When activated the color scheme for your diagrams is automatically toggled
      # based on the selected theme. Supports classic mkdocs and mkdocs-material.
      darkmode: true 
  
      # Highlight color for hyperlinks
      # When a diagram element has a hyperlink on it, the element is highlighted
      # on mouse hover over to better indicate a hyperlink is present.
      highlight: "#0000FF"

      # Enable to open the lightbox on click
      lightbox: true

      # Toolbar specific options
      toolbar:
        # Display the page selector
        pages: true

        # Display the tags selector
        tags: true

        # Display the zoom controls
        zoom: true

        # Display the layer controls
        layers: true

        # Display the lightbox / fullscreen button
        lightbox: true

        # Position of the toolbar (top/bottom)
        position: "top"

        # Do not hide the toolbar when not hovering over diagrams
        no_hide: false
```

## Material Integration

If you are using the Material Theme and want to use the [instant-loading](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/?h=instant#instant-loading) feature. You will have to configure the following:

In your `mkdocs.yaml`:

```yaml
theme:
  name: material
  features:
    - navigation.instant

plugins:
  - drawio

extra_javascript:
  - https://viewer.diagrams.net/js/viewer-static.min.js
  - javascripts/drawio-reload.js
```

Add `docs/javascripts/drawio-reload.js` to your project:

```js
document$.subscribe(({ body }) => {
  GraphViewer.processElements()
})
```
