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
      # Control if hovering on a diagram shows a toolbar for zooming or not
      toolbar: true

      # Control if tooltips will be shown (data-tooltips)
      tooltips: true

      # Increase or decrease the padding around your diagrams
      # (data-border)
      border: 5

      # Control if edit button will be shown in the lightbox view
      # (data-edit)
      edit: true
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
