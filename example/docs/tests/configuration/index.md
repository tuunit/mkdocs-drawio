# Customizations

## Toolbar settings

### Pages

Page selector can be enabled to allow users to navigate between pages. You can use the `toolbar.pages: true|false` config flag in your `mkdocs.yml` or the `data-toolbar-pages` attribute to control if the page selector should be shown or not

![](layers.drawio){ data-toolbar-pages="true" data-nohide="true" }

```md
![](layers.drawio){ data-toolbar-pages="true" }
```

```yml
plugins:
  - drawio:
      toolbar:
        pages: true
```

### Zoom Control

You can use the `zoom: true|false` config flag in your `mkdocs.yml` to control if the zoom control should be shown or not:

![](layers.drawio){ data-toolbar-zoom="true" data-nohide="true" }

```md
![](layers.drawio){ data-toolbar-zoom="true" }
```

```yml
plugins:
  - drawio:
      toolbar:
        zoom: true
```

### Show/Hide Layers

![](layers.drawio){ data-toolbar-layers="true" data-nohide="true" }

```md
![](layers.drawio){ data-toolbar-layers="true" }
```

```yml
plugins:
  - drawio:
      toolbar:
        layers: true
```

### Lightbox button

![](layers.drawio){ data-toolbar-lightbox="true" data-nohide="true" }

```md
![](layers.drawio){ data-toolbar-lightbox="true" }
```

```yml
plugins:
  - drawio:
      toolbar:
        lightbox: true
```

### Toolbar position

Hover on the diagram to see the toolbar at the bottom of the diagram:

![](layers.drawio){ data-toolbar-position="bottom" data-toolbar-pages="true" data-toolbar-lightbox="true" data-toolbar-zoom="true" }

```md
![](layers.drawio){ data-toolbar-position="bottom" }
```

```yml
plugins:
  - drawio:
      toolbar:
        position: 'bottom' # top|bottom
```

## Tooltips

You should be able to use the `tooltips: true|false` config flag in your `mkdocs.yml` to control if tooltips should be shown or not:

![](layers.drawio){ data-tooltips="true"}


## Edit button

You should be able to use the `edit: true|false` config flag in your `mkdocs.yml` to control if the edit button will be shown in the lightbox view of your diagrams. You can also use the `edit` attribute in your diagram to control this:

![](tooltips.drawio){ data-edit="false" zoom="false" }

```md
![](tooltips.drawio){ edit="false" }
```

## Math expressions

Draw.io is great it allows you to use math expressions in your diagrams. Did you know that?

![](math.drawio)
