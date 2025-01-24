# Configuration

## Diagram options

By default the plugin uses the official url for the minified drawio javascript library. To use a custom source for the drawio viewer you can overwritte the url. This might be useful in airlocked environments.

```yaml
plugins:
  - drawio:
      viewer_js: "https://viewer.diagrams.net/js/viewer-static.min.js"
```

Further options are the following with their default value

```yaml
plugins:
  - drawio:
      # Control if hovering on a diagram shows a toolbar for zooming or not
      toolbar:
        # Display the zoom control (data-toolbar-zoom)
        zoom: true

        # Display the page selector (data-toolbar-pages)
        pages: true

        # Display the layers control (data-toolbar-layers)
        layers: true

        # Display the lightbox button (data-toolbar-lightbox)
        lightbox: true

        # Do not hide the toolbar when hovering over the diagram
        # (data-toolbar-nohide)
        nohide: false

        # Control the position of the toolbar (top or bottom)
        # (data-toolbar-position)
        position: "top"

      # Control if tooltips will be shown (data-tooltips)
      tooltips: true

      # Control if edit button will be shown in the lightbox view
      # (data-edit)
      edit: true

      # Increase or decrease the padding around your diagrams
      # (data-border)
      border: 5

      # Use the alt text as page name
      alt_as_page: false
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

## Page selection

Additionally this plugin supports multi page diagrams by using either the `page` or `alt` property. To use the `page` property, you need to use the markdown extension `attr_list`.

By default this attribute is `True`. If you use other plugins such as `mkdocs-caption` you might want to keep `alt` for the caption.

=== "`alt_as_page: True`"

    ```markdown
    ![Page-2](my-diagram.drawio)
    ![my-custom-page-name](my-diagram.drawio)
    ```

=== "`alt_as_page: False`"

    ```markdown
    ![Foo Diagram](my-diagram.drawio){ page="Page-2" }
    ![Bar Diagram](my-diagram.drawio){ page="my-custom-page-name" }
    ```

In your `mkdocs.yml` you can configure the plugin to use the `alt` property instead of the `page` property:

```yaml
markdown_extensions:
  - attr_list
plugins:
  - drawio:
      alt_as_page: False
```
