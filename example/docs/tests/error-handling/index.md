# Error Handling

In the following case the diagram is not valid should show an error message `Not a diagram file`.

## Example

![](test.drawio)


Additionnaly, you should see a warning in your MkDocs server similar to:

```bash
WARNING -  Warning: Found 0 results for page name 'test diagram' for diagram 'test.drawio' on path '/tmp/mkdocs_ce1qjhyn/test2'
ERROR   -  Error: Provided diagram file 'test.drawio' on path '/tmp/mkdocs_ce1qjhyn/test5' is not a valid diagram
```

## Markdown

```markdown
![](test.drawio)
```

