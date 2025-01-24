# Error Handling

In the case your diagram is not valid an error message `Not a diagram file` will be displayed in the rendered page :

![](test.drawio)

```md
![](test.drawio)
```

Additionnaly, you will see a warning in your MkDocs server similar to:

```text
WARNING -  Found 0 results for page name 'test diagram'
           for diagram 'test.drawio' on path '/tmp/mkdocs_ce1qjhyn/test2'
ERROR   -  Provided diagram file 'test.drawio' on path
           '/tmp/mkdocs_ce1qjhyn/test5' is not a valid diagram
```
