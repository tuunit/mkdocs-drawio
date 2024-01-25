# MkDocs Plugin for embedding Drawio files
[![Publish Badge](https://github.com/tuunit/mkdocs-drawio/workflows/Publish/badge.svg)](https://github.com/tuunit/mkdocs-drawio/actions)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-drawio)](https://pypi.org/project/mkdocs-drawio/)

[Buy Sergey a 🍜](https://www.buymeacoffee.com/SergeyLukin)

## Features
This plugin enables you to embed interactive drawio diagrams in your documentation. Simply add your files like you would any other image:

```markdown
![](my-diagram.drawio)
```

Additionally this plugin supports multi page diagrams by using the `alt` text to select the pages by name:

```markdown
![Page-2](my-diagram.drawio)
![my-custom-page-name](my-diagram.drawio)
```

## Setup

Install plugin using pip:

```
pip install mkdocs-drawio
```

Add the plugin to your `mkdocs.yml`

```yaml
plugins:
  - drawio
```

### Configuration

To use a custom source for the drawio viewer JavaScript file you can overwritte the url.

```yaml
plugins:
  - drawio:
      viewer_js: "https://viewer.diagrams.net/js/viewer-static.min.js"
```

## How it works

After mkdocs has generated the html for your documentation, this plugin adds the necessary drawio javascript library. Searches for `img` tags with a file ending of `*.drawio` and replaces them with the appropiate `mxgraph` html block. For further details, please have a look at the [official drawio.com documentation](https://www.drawio.com/doc/faq/embed-html).
