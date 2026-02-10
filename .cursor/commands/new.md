## Command: /new

This command will create a new interactive guide in JSON format. To do this, you will:

1. Prompt the user to give you the name of the tutorial
2. Create a directory for that tutorial under the root, using dashed-names as
the other directories do. If a user creates a tutorial called "First k6 Test"
this would become a directory called first-k6-test.
3. Create a file called `content.json` under that directory
4. Into that file, place a minimal JSON guide scaffold like this:

```json
{
  "id": "guide-id",
  "title": "Guide Title",
  "blocks": [
    {
      "type": "markdown",
      "content": "Introduction text goes here."
    },
    {
      "type": "section",
      "id": "section-1",
      "title": "First Section",
      "blocks": []
    }
  ]
}
```

5. Update the `id` field to match the directory name
6. Update the `title` field to match the user's chosen tutorial name
7. Remind the user to consult docs/json-guide-format.md for the full format reference

> **Note**: The HTML format (`unstyled.html`) is deprecated. All new guides must use the JSON format (`content.json`).
