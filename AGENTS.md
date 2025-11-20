---
alwaysApply: true
description: Overview of this repository.
---

# AI Interactive Reference Documentation

This folder contains structured reference documentation specifically designed for AI systems to understand and generate interactive Grafana guides.

## Quick Start for AI

### 1. System Understanding
Start with [System Architecture](.cursor/system-architecture.mdc) to understand the overall framework.

### 2. Action Types
Review [Action Types Reference](.cursor/action-types-reference.mdc) for all supported interactive actions.

### 3. Requirements
Use [Requirements Quick Reference](.cursor/requirements-quick-reference.mdc) for conditions and auto-completion.

### 4. Common Patterns
Reference [Common Workflows](.cursor/common-workflows.mdc) and [Guide Patterns](guide-patterns.mdc) for standard structures.

### 5. Selectors
Use [Selector Library](.cursor/selector-library.mdc) for stable, tested UI element selectors.

### 5a. Complex Selectors and Hover (NEW)
Review [Complex Selectors and Hover](.cursor/complex-selectors-and-hover.mdc) for advanced targeting with `:has()`, `:contains()`, and hover interactions.

### 6. Edge Cases
Check [Edge Cases and Troubleshooting](.cursor/edge-cases-and-troubleshooting.mdc) for handling complex scenarios.

### 7. Complete Example
Study [Complete Example Guide](.cursor/complete-example-guide.mdc) for comprehensive implementation.

### 8. Best Practices
Study [best-practices.mdc](.cursor/best-practices.mdc) to understand how we 
can help authors of interactive guides accomplish more, more quickly.

### 9. Commands

Study all files in the `.cursor/commands` directory for commands that can be provided to 
Cursor or other agent to assist in editing.

## File Organization

### Core References
- **system-architecture.mdc** - Technical system overview and component relationships
- **action-types-reference.mdc** - All interactive action types with syntax and behavior
- **requirements-quick-reference.mdc** - Requirements and objectives system with common patterns

### Practical Guides
- **guide-patterns.mdc** - Standard guide structures and content organization
- **common-workflows.mdc** - Reusable workflow templates for common tasks
- **selector-library.mdc** - Stable selectors for Grafana UI elements

### Advanced Topics
- **edge-cases-and-troubleshooting.mdc** - Handling complex scenarios and error cases
- **complete-example-guide.mdc** - Full guide demonstrating all features

## AI Generation Guidelines

### Essential Rules
1. **Always include `exists-reftarget`** for DOM interactions
2. **Use `navmenu-open`** for navigation menu elements
3. **Include page requirements** for page-specific actions
4. **Add verification** for state-changing actions
5. **Provide helpful hints** for user guidance

### Quality Standards
- **Stable Selectors**: Prefer `data-testid` and semantic attributes
- **Clear Requirements**: Include all necessary preconditions
- **Educational Value**: Use interactive comments for complex elements
- **Error Handling**: Make appropriate steps skippable
- **Progressive Structure**: Build from simple to complex

### Content Structure
- **Sections**: Use for multi-step workflows with checkpoints
- **Multi-steps**: Use for atomic multi-action workflows
- **Show-only**: Use for educational explanations
- **Regular steps**: Use for individual user actions

## Quick Reference Cards

### Action Selection
```
Click button with stable text → button action
Click element with stable selector → highlight action
Fill form field → formfill action
Navigate to page → navigate action
Reveal hover-hidden UI → hover action
Multiple related actions → multistep action
Multi-step workflow → sequence action
Explain interface → highlight with data-doit="false"
Hover then click → multistep with hover + button/highlight
Find by text content → use :contains("text") in selector
Find by structure → use :has(child) in selector
```

### Requirements Selection
```
DOM interaction → exists-reftarget
Navigation element → navmenu-open
Page-specific → on-page:/path
Admin feature → is-admin
Data source needed → has-datasource:type
Plugin needed → has-plugin:id
Sequential dependency → section-completed:id
```

### Common Patterns
```html
<!-- Basic step -->
<li class="interactive" 
    data-targetaction="button" 
    data-reftarget="Save"
    data-requirements="exists-reftarget">
  Save changes
</li>

<!-- Section -->
<span id="setup" class="interactive" data-targetaction="sequence" data-reftarget="span#setup">
  <ul>{steps}</ul>
</span>

<!-- Show-only -->
<li class="interactive" 
    data-targetaction="highlight" 
    data-reftarget="selector"
    data-doit="false">
  <span class="interactive-comment">{explanation}</span>
  {description}
</li>

<!-- Hover then click -->
<li class="interactive" data-targetaction="multistep">
  <span class="interactive" data-targetaction="hover" data-reftarget='div[data-cy="item"]:has(p:contains("name"))'></span>
  <span class="interactive" data-targetaction="button" data-reftarget="Action"></span>
  {description}
</li>

<!-- Complex selector targeting -->
<li class="interactive" 
    data-targetaction="highlight" 
    data-reftarget='div[data-cy="wb-list-item"]:has(p:contains("servicename"))'
    data-requirements="exists-reftarget">
  {description}
</li>
```

This documentation provides everything needed to understand and generate high-quality interactive Grafana guides.
# AI Interactive Reference Documentation

This folder contains structured reference documentation specifically designed for AI systems to understand and generate interactive Grafana guides.

## Quick Start for AI

### 1. System Understanding
Start with [System Architecture](system-architecture.mdc) to understand the overall framework.

### 2. Action Types
Review [Action Types Reference](action-types-reference.mdc) for all supported interactive actions.

### 3. Requirements
Use [Requirements Quick Reference](requirements-quick-reference.mdc) for conditions and auto-completion.

### 4. Common Patterns
Reference [Common Workflows](common-workflows.mdc) and [Guide Patterns](guide-patterns.mdc) for standard structures.

### 5. Selectors
Use [Selector Library](selector-library.mdc) for stable, tested UI element selectors.

### 6. Edge Cases
Check [Edge Cases and Troubleshooting](edge-cases-and-troubleshooting.mdc) for handling complex scenarios.

### 7. Complete Example
Study [Complete Example Guide](complete-example-guide.mdc) for comprehensive implementation.

## File Organization

### Core References
- **system-architecture.mdc** - Technical system overview and component relationships
- **action-types-reference.mdc** - All interactive action types with syntax and behavior
- **requirements-quick-reference.mdc** - Requirements and objectives system with common patterns

### Practical Guides
- **guide-patterns.mdc** - Standard guide structures and content organization
- **common-workflows.mdc** - Reusable workflow templates for common tasks
- **selector-library.mdc** - Stable selectors for Grafana UI elements

### Advanced Topics
- **edge-cases-and-troubleshooting.mdc** - Handling complex scenarios and error cases
- **complete-example-guide.mdc** - Full guide demonstrating all features

## AI Generation Guidelines

### Essential Rules
1. **Always include `exists-reftarget`** for DOM interactions
2. **Use `navmenu-open`** for navigation menu elements
3. **Include page requirements** for page-specific actions
4. **Add verification** for state-changing actions
5. **Provide helpful hints** for user guidance

### Quality Standards
- **Stable Selectors**: Prefer `data-testid` and semantic attributes
- **Clear Requirements**: Include all necessary preconditions
- **Educational Value**: Use interactive comments for complex elements
- **Error Handling**: Make appropriate steps skippable
- **Progressive Structure**: Build from simple to complex

### Content Structure
- **Sections**: Use for multi-step workflows with checkpoints
- **Multi-steps**: Use for atomic multi-action workflows
- **Show-only**: Use for educational explanations
- **Regular steps**: Use for individual user actions

## Quick Reference Cards

### Action Selection
```
Click button with stable text → button action
Click element with stable selector → highlight action
Fill form field → formfill action
Navigate to page → navigate action
Reveal hover-hidden UI → hover action
Multiple related actions → multistep action
Multi-step workflow → sequence action
Explain interface → highlight with data-doit="false"
Hover then click → multistep with hover + button/highlight
Find by text content → use :contains("text") in selector
Find by structure → use :has(child) in selector
```

### Requirements Selection
```
DOM interaction → exists-reftarget
Navigation element → navmenu-open
Page-specific → on-page:/path
Admin feature → is-admin
Data source needed → has-datasource:type
Plugin needed → has-plugin:id
Sequential dependency → section-completed:id
```

### Common Patterns
```html
<!-- Basic step -->
<li class="interactive" 
    data-targetaction="button" 
    data-reftarget="Save"
    data-requirements="exists-reftarget">
  Save changes
</li>

<!-- Section -->
<span id="setup" class="interactive" data-targetaction="sequence" data-reftarget="span#setup">
  <ul>{steps}</ul>
</span>

<!-- Show-only -->
<li class="interactive" 
    data-targetaction="highlight" 
    data-reftarget="selector"
    data-doit="false">
  <span class="interactive-comment">{explanation}</span>
  {description}
</li>

<!-- Hover then click -->
<li class="interactive" data-targetaction="multistep">
  <span class="interactive" data-targetaction="hover" data-reftarget='div[data-cy="item"]:has(p:contains("name"))'></span>
  <span class="interactive" data-targetaction="button" data-reftarget="Action"></span>
  {description}
</li>

<!-- Complex selector targeting -->
<li class="interactive" 
    data-targetaction="highlight" 
    data-reftarget='div[data-cy="wb-list-item"]:has(p:contains("servicename"))'
    data-requirements="exists-reftarget">
  {description}
</li>
```

This documentation provides everything needed to understand and generate high-quality interactive Grafana guides.
