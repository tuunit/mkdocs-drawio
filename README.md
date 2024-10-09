# MkDocs Plugin for embedding Drawio files
[![Publish Badge](https://github.com/tuunit/mkdocs-drawio/workflows/Publish/badge.svg)](https://github.com/tuunit/mkdocs-drawio/actions)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-drawio)](https://pypi.org/project/mkdocs-drawio/)

[Buy Sergey a ☕](https://www.buymeacoffee.com/SergeyLukin) 

Sergey ([onixpro](https://github.com/onixpro)) is the original creator of this plugin. Repo can be found [here.](https://github.com/onixpro/mkdocs-drawio-file)

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
      toolbar: true  # control if hovering on a diagram shows a toolbar for zooming or not (default: true)
      tooltips: true # control if tooltips will be shown (default: true)
      border: 10     # increase or decrease the border / margin around your diagrams (default: 5) 
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

1. Either use the devcontainer or setup a venv with mkdocs installed
2. Install your current local version: `pip install -e .`
3. Add a test for your changes in the `example` directory
4. Test your changes by starting `mkdocs serve` in the `example` directory
5. Increase the version `pyproject.toml`
6. Open pull request
