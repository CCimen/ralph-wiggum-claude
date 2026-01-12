---
description: "Add a guardrail (learned constraint) that prevents a mistake from happening again. Usage: /ralph-loop:sign <rule>. Example: /ralph-loop:sign Always run tests before committing"
---

# Add Ralph Guardrail

The user wants to add a guardrail (learned constraint) manually. Guardrails prevent repeating the same mistakes.

## Usage

```
/ralph-loop:sign [guardrail text]
```

Example:
```
/ralph-loop:sign Always check if file exists before reading
/ralph-loop:sign Run npm install after modifying package.json
/ralph-loop:sign Use async/await instead of callbacks in this codebase
```

## Implementation

### 1. Parse the Guardrail

Extract the guardrail text from: $ARGUMENTS

If $ARGUMENTS is empty, use AskUserQuestion:
"What guardrail would you like to add? Describe the constraint or rule to follow."

### 2. Get Current Iteration

Read `.ralph/ralph_task.md` to get current iteration number.

### 3. Append to Guardrails

Add to `.ralph/guardrails.md`:

```markdown

### Sign: [guardrail text]
- **Trigger**: User-added constraint
- **Added**: Iteration [N] (manual)
```

### 4. Log the Addition

Append to `.ralph/errors.log`:
```
[timestamp] GUARDRAIL_ADDED "[guardrail text]" source=manual iteration=[N]
```

### 5. Confirm

Output:
```
Guardrail added: "[guardrail text]"

This constraint will be checked before every action.
Current guardrails: [total count]
```

## When to Add Guardrails

Encourage users to add guardrails when they notice:
- Patterns that cause problems
- Codebase-specific conventions
- Dependencies between operations
- Common pitfalls they want to avoid
