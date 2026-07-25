# MkDocs Plugin for embedding Drawio files

<img width="256" height="256" alt="Image" src="https://github.com/user-attachments/assets/fb25d409-38eb-4e1a-90e8-6db78999514e" />

[![Publish Badge](https://github.com/tuunit/mkdocs-drawio/workflows/Publish/badge.svg)](https://github.com/tuunit/mkdocs-drawio/actions)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-drawio)](https://pypi.org/project/mkdocs-drawio/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-drawio)

See the [official docs](https://tuunit.github.io/mkdocs-drawio/) and the [live example page](https://tuunit.github.io/mkdocs-drawio/tests/simple-diagram/).

## Features

This plugin enables you to embed interactive drawio diagrams in your documentation. Simply add your diagrams like you would any other image:

```markdown
You can either use diagrams hosted within your own docs. Absolute as well as relative paths are allowed:

Absolute path:
![](/assets/my-diagram.drawio)

Same directory as the markdown file:
![](my-diagram.drawio)

Relative directory to the markdown file:
![](../my-diagram.drawio)


Or you can use external urls:
![](https://example.com/diagram.drawio)
```

Additionally this plugin supports multi page diagrams by using either the `page` or `alt` property. To use the `page` property, you need to use the markdown extension `attr_list`.

```markdown
Either use the alt text:
![Page-2](my-diagram.drawio)
![my-custom-page-name](my-diagram.drawio)

Or use the page attribute:
![Foo Diagram](my-diagram.drawio){ page="Page-2" }
![Bar Diagram](my-diagram.drawio){ page="my-custom-page-name" }
```

## Setup

Install the plugin with pip:

```bash
pip install mkdocs-drawio
```

If you are managing your MkDocs project with uv, use:

```bash
uv add mkdocs-drawio
```

Add the plugin to your `mkdocs.yml`

```yaml
plugins:
  - drawio
```

## Configuration Options

Full documentation of the configuration options and examples can be found in the [official documentation](https://tuunit.github.io/mkdocs-drawio/)

By default the plugin uses the official url for the minified drawio javascript library. To use a custom source for the drawio viewer you can overwritte the url. This might be useful in airlocked environments.

> If you want to use a self-hosted JavaScript viewer file. You should download the latest version from the [official drawio repo](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/js/viewer-static.min.js).

Self-hosted viewer paths can be configured as site-root paths such as `js/viewer-static.min.js`. The plugin normalizes them per page, so they also work on versioned deployments such as `mike`.

```yaml
plugins:
  - drawio:
      viewer_js: "https://viewer.diagrams.net/js/viewer-static.min.js"
```

Further options are:

```yaml
plugins:
  - drawio:
      tooltips: true       # Enable tooltips on diagram elements
      border: 5            # Border size / padding around diagrams
      edit: true           # Enable opening the editor for diagrams
      darkmode: true       # Enable dark mode support (classic MkDocs and Material)
      highlight: "#0000FF" # Highlight color for hyperlinks
      lightbox: true       # Enable opening the lightbox on click
      toolbar:             # Control the looks and behaviour of the toolbar
        pages: true        # Display the page selector
        tags: true         # Display the tags selector
        zoom: true         # Display the zoom controls
        layers: true       # Display the layer controls
        lightbox: true     # Display the lightbox / fullscreen button
        position: "top"    # Control the position of the toolbar (top or bottom)
        no_hide: false     # Do not hide the toolbar when not hovering over diagrams
        show_title: false  # Show the diagram title in the toolbar based on the file name
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
  // if drawio toolbar icons/buttons are not showing or missing due to title being longer than the image width
  // you can set a minimum width for the graph viewer by uncommenting the following line
  // GraphViewer.prototype.minWidth = 500;

  GraphViewer.processElements()

  // required to fix duplicate display of external drawio graphs (via http)
  reload();
})
```

## Using Tabs (pymdownx.tabbed)

If you want to use drawio diagrams inside of tabs you need to make sure that the diagrams are processed after the tabs are rendered. You can achieve this by adding the following javascript to your `mkdocs.yml`:

```yaml
extra_javascript:
  - javascripts/drawio-tabs.js
```

Add `docs/javascripts/drawio-tabs.js` to your project:

```js
document.addEventListener('change', (event) => {
  // Check if the target is a pymdownx tab input
  if (event.target.matches('.tabbed-set > input')) {
    GraphViewer.processElements()
  }
});
```

Its a bit of a workaround as it listens for all events on the page and retriggers the drawio processing if any tab is clicked.


## How it works

1. mkdocs generates the html per page
2. `mkdocs-drawio` attaches to the `on_post_page` event. For more details, please have a look at the [event lifecycle documentation](https://www.mkdocs.org/dev-guide/plugins/#events)
3. Adds the drawio viewer library
4. Searches through the generated html for all `img` tags that have a source of type `.drawio`
5. Replaces the found `img` tags with `mxgraph` html blocks (actual drawio diagram content). For more details, please have a look at the [official drawio.com documentation](https://www.drawio.com/doc/faq/embed-html).

## Contribution guide

1. Install uv and use Python 3.9 or newer.
2. Install dependencies and the current project: `uv sync --group dev`
3. Make your desired changes.
4. Add a test for your changes in the `examples` directory.
5. Test your changes with `uv run mkdocs serve -f examples/mkdocs.yml`
6. Increase the version in `pyproject.toml`.
7. Make sure `uv run ruff check .` and `uv run black --check .` pass.
8. Open your pull request ✨️

## Project History

Sergey ([onixpro](https://github.com/onixpro)) is the original creator of this plugin but since his repository isn't maintained anymore we forked it on the 19th December of 2023 and have been keeping it up-to-date and expanding on the features since then. 
[Buy Sergey a ☕](https://www.buymeacoffee.com/SergeyLukin) 
