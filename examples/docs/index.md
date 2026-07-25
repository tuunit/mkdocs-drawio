# MkDocs Plugin for embedding Drawio files

This plugin allows you to embed draw.io diagrams in your MkDocs documentation. It is compatible with most MkDocs themes, but specifically tested with the Material theme and the MkDocs default theme.

<img width="256" height="256" alt="Image" src="https://github.com/user-attachments/assets/fb25d409-38eb-4e1a-90e8-6db78999514e" />

## Installation

Install the plugin with pip:

```bash
pip install mkdocs-drawio
```

If you are managing your MkDocs project with uv, use:

```bash
uv add mkdocs-drawio
```

Then add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - drawio
```

## Features

The currently supported features are:

* Embed draw.io diagrams as normal markdown images in your documentation.
* Use diagrams hosted within your own docs or external urls.
* Support for multi page diagrams by selecting which page to display.
* Compatible with `mkdocs-caption` and `mkdocs-glightbox`.
* Print and edit button.
* Dark Mode 🕶️

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

Additionally this plugin supports multi page diagrams by using the `alt` text to select the pages by name:

```markdown
![Page-2](my-diagram.drawio)
![my-custom-page-name](my-diagram.drawio)
```


## Project History

Sergey ([onixpro](https://github.com/onixpro)) is the original creator of this plugin but since his repository isn't maintained anymore we forked it on the 19th December of 2023 and have been keeping it up-to-date and expanding on the features since then. 
[Buy Sergey a ☕](https://www.buymeacoffee.com/SergeyLukin) 
