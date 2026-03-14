# Style diagrams

## Examples

- Set background colour to green  
  `style="background-color: green;"`

![](test.drawio){ style="background-color: green;"}

- Center diagram  
  `style="margin: auto;"`

![](test.drawio){ style="margin: auto;"}

!!! note annotate

    Styles, which change the size of the diagram like `style="zoom: 0.5"`, are
    not recommended to use with the style option because the minified drawio
    javascript library creates and destroys the toolbar outside the mxgraph
    diagram container. Meaning the toolbar does not get styled too.

    Use the [zoom option](../zoom-diagram/index.md) instead.

## Markdown

```markdown
![](test.drawio){ style="$STYLE_STRING" }
```
