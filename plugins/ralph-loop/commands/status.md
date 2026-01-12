---
description: "Display Ralph Loop progress: task overview, completion percentage, current phase, blockers, and active guardrails. Shows what's done, what's next, and any constraints learned."
---

# Ralph Loop Status

Read and display the current state of the Ralph Loop. If `.ralph/` directory doesn't exist, inform the user to run `/ralph-loop:start` first.

## Status Report Format

### 1. Task Overview (from ralph_task.md)

Read `.ralph/ralph_task.md` and display:
- Task description from frontmatter
- Current iteration number
- Status (in_progress/completed/blocked)
- Success criteria with checkbox status:
  ```
  Success Criteria: 3/7 completed
  [x] Criterion 1
  [x] Criterion 2
  [x] Criterion 3
  [ ] Criterion 4 (current)
  [ ] Criterion 5
  [ ] Criterion 6
  [ ] Criterion 7
  ```

### 2. Current Progress (from progress.md)

Read `.ralph/progress.md` and display:
- Current phase
- Last completed action
- What's currently in progress
- What's next up
- Any blockers

### 3. Guardrails Summary (from guardrails.md)

Read `.ralph/guardrails.md` and display:
- Total number of active guardrails
- List the most recent 3 guardrails (if any)

### 4. Recent Activity (from errors.log)

Read the last 5 lines of `.ralph/errors.log` and show:
- Recent errors (if any)
- Any rotation triggers
- Recently added guardrails

## Output Format

```
=== Ralph Loop Status ===

Task: [task description]
Iteration: [N] | Status: [status]

Progress: [X]/[Y] criteria completed
[checkbox list]

Current Phase: [phase]
Last Action: [action]
In Progress: [what's being worked on]
Blocked By: [blockers or "None"]

Guardrails: [N] active
[list recent guardrails if any]

Recent Errors: [count or "None"]
[list if any]
```
