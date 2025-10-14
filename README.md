# MkDocs Plugin for embedding Drawio files

[![Publish Badge](https://github.com/tuunit/mkdocs-drawio/workflows/Publish/badge.svg)](https://github.com/tuunit/mkdocs-drawio/actions)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-drawio)](https://pypi.org/project/mkdocs-drawio/)

Sergey ([onixpro](https://github.com/onixpro)) is the original creator of this plugin but since his repository isn't maintained anymore we forked it on the 19th December of 2023 and have been keeping it up-to-date and expanding on the features since then. 
[Buy Sergey a ☕](https://www.buymeacoffee.com/SergeyLukin) 

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

Install plugin using pip:

```bash
pip install mkdocs-drawio
```

Add the plugin to your `mkdocs.yml`

```yaml
plugins:
  - drawio
```

## Configuration Options

By default the plugin uses the official url for the minified drawio javascript library. To use a custom source for the drawio viewer you can overwritte the url. This might be useful in airlocked environments.

> If you want to use a self-hosted JavaScript viewer file. You should download the latest version from the [official drawio repo](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/js/viewer-static.min.js).

```yaml
plugins:
  - drawio:
      viewer_js: "https://viewer.diagrams.net/js/viewer-static.min.js"
```

Further options are:

```yaml
plugins:
  - drawio:
      toolbar: true        # control if hovering on a diagram shows a toolbar for zooming or not (default: true)
      tooltips: true       # control if tooltips will be shown (default: true)
      edit: true           # control if edit button will be shown in the lightbox view (default: true)
      border: 10           # increase or decrease the border / margin around your diagrams (default: 0)
      darkmode: true       # support darkmode. allows for automatic switching between dark and lightmode based on the theme toggle. (default: false)
      highlight: "#0000FF" # color hyperlinks on mouse hover over (default: no color)
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

## How it works

1. mkdocs generates the html per page
2. `mkdocs-drawio` attaches to the `on_post_page` event. For more details, please have a look at the [event lifecycle documentation](https://www.mkdocs.org/dev-guide/plugins/#events)
3. Adds the drawio viewer library
4. Searches through the generated html for all `img` tags that have a source of type `.drawio`
5. Replaces the found `img` tags with `mxgraph` html blocks (actual drawio diagram content). For more details, please have a look at the [official drawio.com documentation](https://www.drawio.com/doc/faq/embed-html).

## Contribution guide

1. Setup a virtual environment: `python3 -m venv venv && source venv/bin/activate`
2. Install poetry: `pip install poetry`
3. Install dependencies and current version: `poetry install`
4. Make your desired changes
5. Add a test for your changes in the `example` directory
6. Test your changes by starting `mkdocs serve` in the `example` directory
7. Increase the version in `pyproject.toml`
8. Make sure `poetry run ruff check .` and `poetry run black --check .` passing
9. Open your pull request ✨️
