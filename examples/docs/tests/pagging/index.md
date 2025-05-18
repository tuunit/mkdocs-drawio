# Pagging

## Examples

Below you should see diagram Page-1:
![Page-1](test.drawio)

Below you should see diagram Page-2:
![Page-2](test.drawio)

Below you should see Page-1 (default) because the specified Page-3 has not been found:
![Page-3](test.drawio)

Furthoremore, you should see a warning in your mkdocs server similar to:

```bash
WARNING -  Warning: Found 0 results for page name 'Page-3' for diagram 'test.drawio' on path '/tmp/mkdocs_ce1qjhyn/test2'
```

## Markdown

```markdown
![Page-1](test.drawio)
![Page-2](test.drawio)
![Page-3](test.drawio)
```
