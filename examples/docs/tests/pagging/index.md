# Pagging

You can either use the `alt` text of the image for pagging or use an attribute
page for pagging if you have the `attr_list` markdown extension installed in 
your `mkdocs.yaml`.

```yaml
markdown_extensions:
  - attr_list
```

## Examples

=== "Diagram"
    Below you should see diagram Page-1:
    ![Page-1](test.drawio)

=== "Markdown"
    ```markdown
    ![Page-1](test.drawio)
    ```

---

=== "Diagram"
    Below you should see diagram Page-2:
    ![Page-2](test.drawio)

=== "Markdown"
    ```markdown
    ![Page-2](test.drawio)
    ```

---

=== "Diagram"
    Below you should see diagram Page-2 using the attribute page:
    ![Some alt text](test.drawio){ page="Page-2" }

=== "Markdown"
    ```markdown
    ![Some alt text](test.drawio){ page="Page-2" }
    ```

---

=== "Diagram"
    Below you should see Page-1 (default) because the specified Page-3 has not been found:
    ![Page-3](test.drawio)
    
    Furthoremore, you should see a warning in your mkdocs server similar to:
    
    ```bash
    WARNING -  Warning: Found 0 results for page name 'Page-3' for diagram 'test.drawio' on path '/tmp/mkdocs_ce1qjhyn/test2'
    ```

=== "Markdown"
    ```markdown
    If page doesn't exist it will fallback to the first page.
    ![Page-3](test.drawio)
    ```
