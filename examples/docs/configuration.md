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
      # control if hovering on a diagram shows a
      # toolbar for zooming or not
      toolbar: true

      # control if tooltips will be shown
      tooltips: true

      # control if edit button will be shown in the
      # lightbox view
      edit: true

      # increase or decrease the border / margin around your diagrams
      border: 0

      # support darkmode. allows for automatic switching
      # between dark and lightmode based on the theme toggle.
      darkmode: false

      # treat the image caption as the diagram page name.
      # Set to true to use the attr_list 'page' attribute instead.
      # this option is not enabled by default to maintain backward
      # compatibility.
      use_page_attribute: false
```

## HTML Attributes

For each global configuration option you can also use the attribute in the diagram itself. This will override the global configuration. Here is an example:

```markdown
![](my-diagram.drawio){ data-toolbar-zoom="false" }
```

To use these attributes you need to enable the markdown extension `attr_list` in your `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
```

> Note: When `use_page_attribute` is set to `true`, enabling the `attr_list` extension becomes mandatory because page selection is driven exclusively through the `page` attribute.

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
