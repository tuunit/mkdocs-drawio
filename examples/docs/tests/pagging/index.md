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
    Below you should see the diagram Page-2 using the page attribute:
    ![Some alt text](test.drawio){ page="Page-2" }

=== "Markdown"
    ```markdown
    ![Some alt text](test.drawio){ page="Page-2" }
    ```

---

=== "Diagram"
    If the alt text doesn't exist as a page it will fallback to the first page of your diagram.
    Below you should therefore see Page-1 (default):
    ![Page-3](test.drawio)

    Furthoremore, you should see a warning in your mkdocs server similar to:

    ```bash
    WARNING -  Warning: Found 0 results for page name 'Page-3' for diagram 'test.drawio' on path '/tmp/mkdocs_ce1qjhyn/test2'
    ```

=== "Markdown"
    ```markdown
    ![Page-3](test.drawio)
    ```

---

=== "Diagram"
    If the alt text and page attribute don't exist as a page, it will fallback to the first page of your diagram.
    Below you should therefore see Page-1 (default):
    ![Some alt text](test.drawio){ page="Page-3" }

    Furthoremore, you should see a warning in your mkdocs server similar to:

    ```bash
    WARNING -  Warning: Found 0 results for page name 'Page-3' for diagram 'test.drawio' on path '/tmp/mkdocs_ce1qjhyn/test2'
    ```

=== "Markdown"
    ```markdown
    ![Some alt text](test.drawio){ page="Page-3" }
    ```

---

=== "Diagram"
    Pagging logic for SVG diagrams is skip as only a single page can be exported as an SVG drawio diagram.

    ![Some alt text](test.drawio.svg){ page="Page-3" }

=== "Markdown"
    ```markdown
    ![Some alt text](test.drawio.svg){ page="Page-3" }
    ```
