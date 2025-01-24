# MkDocs Drawio Plugin

This plugin allows you to embed draw.io diagrams in your MkDocs documentation. It is compatible with most MkDocs themes, but specifically tested with the Material theme and the MkDocs default theme.

Sergey ([onixpro](https://github.com/onixpro)) is the original creator of this plugin. Repo can be found [here.](https://github.com/onixpro/mkdocs-drawio-file)

## Installation

Install the plugin using pip or poetry:

```bash
pip install mkdocs-drawio
```

or

```bash
poetry add mkdocs-drawio
```

Then add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - drawio
```

## Features

The currently supported features are:

- Embed draw.io diagrams in your documentation to keep a single source of truth.
- Use diagrams hosted within your own docs or external urls.
- Support for multi page diagrams by selecting which page to display.
- Compatible with `mkdocs-caption` and `mkdocs-glightbox`.
- Match the diagram theme with your MkDocs theme (light, dark/slate).
- Zoom in/out.
- Full screen preview.
- Print or edit button.

## Usage

Simply add an image as you would normally do in markdown:

```markdown
Absolute path:
![](/assets/my-diagram.drawio)

Same directory as the markdown file:
![](my-diagram.drawio)

Relative directory to the markdown file:
![](../my-diagram.drawio)

Or you can use external urls:
![](https://example.com/diagram.drawio)
```
