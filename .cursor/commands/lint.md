## Command: /lint

When an author tells you /lint, you will execute the following checklist
to validate a piece of content being written.

1. Check that the file is valid JSON and can be parsed without errors
2. Check that the root structure has required fields: `id`, `title`, `blocks`
3. Check that all block types are valid (`markdown`, `interactive`, `section`,
`multistep`, `guided`, `conditional`, `quiz`, `input`, `image`, `video`, `html`,
`assistant`, `code-block`, `terminal`, `terminal-connect`, `grot-guide`)
4. Check that all action types are valid (`highlight`, `button`, `formfill`,
`navigate`, `hover`, `noop`, `popout`)
5. Check that required properties are present for each block type (e.g.,
`action` and `reftarget` for interactive blocks, `id` and `title` for sections).
For `popout` actions, verify `targetvalue` is present and equals `"sidebar"` or
`"floating"` (anything else is rejected by the schema).
6. Check that the selectors and testids are appropriately used and follow
best practices (prefer `data-testid` over CSS classes)
7. Check that requirements are valid and well-formed (see docs/requirements-reference.md)
8. Check for misspellings and typos in property names and string values
9. Check all CSS selectors and verify they follow best practices
10. Verify that `navmenu-open` is used for navigation menu elements and
`on-page:` requirements are used for page-specific actions
11. Check that any step targeting a virtualised container (long tables, paginated
lists, dashboard rows below the fold) is inside a `guided` block with
`lazyRender: true` on the step. Plain `interactive` will fail there.
12. Check that `navigate` actions chaining to another guide use the `openGuide`
field (`"openGuide": "bundled:<guide-id>"`), not the legacy `?doc=` query param.
