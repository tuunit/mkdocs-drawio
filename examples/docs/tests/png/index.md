# PNG diagram

## Example

=== "Diagram"

The following is a PNG based drawio diagram:

![](test.drawio.png)

You can open the diagram as an PNG in your browser. [Click here.](test.drawio.png)

If the PNG file contains no mxfile information, then it'll fail and fall back to the "Not a diagram file" error being displayed in-place of the diagram:

![](missing-mxfile.drawio.png)

With the following server error:

```bash
ERROR   -  Error: Could not parse diagram file '../tests/png/missing-mxfile.drawio.png' on path '/tmp/mkdocs_3kdph6pm/print_page': argument of type 'NoneType' is not iterable
```

=== "Markdown"

```markdown
![](test.drawio.png)
```