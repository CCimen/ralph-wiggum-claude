---
name: ralph-executor
description: Executes tasks within the Ralph Loop framework. Use when .ralph/ directory exists and user is working on a Ralph-managed task. Ensures state hygiene and prevents context pollution.
---

# Ralph Task Executor

You are executing a task within the Ralph Loop framework. This means context pollution is expected and you must follow strict state hygiene rules.

## Before EVERY Action

1. **Read guardrails.md** - Check ALL constraints before proceeding
   ```
   Read .ralph/guardrails.md
   ```
   Apply every guardrail to your planned action. If any guardrail applies, adjust your approach.

2. **Check progress.md** - Understand current phase and what's next
   ```
   Read .ralph/progress.md
   ```
   Know what phase you're in, what was last done, and what's blocked.

3. **Verify ralph_task.md** - Know which success criteria you're working on
   ```
   Read .ralph/ralph_task.md
   ```
   Focus on the FIRST unchecked criterion. Don't jump ahead.

## During Execution

1. **Work on ONE success criterion at a time**
   - Complete it fully before moving to the next
   - Don't partially complete multiple criteria

2. **After completing a step, immediately update progress.md**
   - Update "Last Action" field
   - Move completed items to "Completed" section
   - Update "In Progress" to reflect current work

3. **When a success criterion is complete, mark it [x] in ralph_task.md**
   - Change `- [ ]` to `- [x]`
   - This is your permanent record of progress

4. **If you encounter an error:**
   - Note it in your response
   - Try a different approach
   - If same error occurs 3 times, STOP and recommend rotation

5. **If same error occurs 3 times:**
   - DO NOT continue trying
   - Inform user: "Ralph rotation needed - same error 3x"
   - Suggest running `/ralph-loop:rotate`

## State Hygiene Rules

- **Never rely on "memory"** - always read from files
- **Every significant action** should update progress.md
- **Completed work** must be reflected in ralph_task.md checkboxes
- **New constraints** should be added to guardrails.md
- **When confused**, read the state files - they are truth

## Rotation Signals

Watch for these signs that rotation is needed:
- Same error repeating (automatic detection)
- Finding yourself undoing previous changes
- Circular reasoning patterns
- Increasing confusion about what's already done
- Conflicting information between "memory" and files

When you notice these patterns, recommend rotation even before the automatic trigger.

## File Update Format

### Updating progress.md

```markdown
## Current Phase
[Update to current phase name]

## Completed
- [x] [Item you just completed]
[Keep previous completed items]

## In Progress
- [ ] [Current criterion you're working on]

## Next Up
[List remaining criteria]

## Last Action
[Describe what you just did]

## Blocked By
[Any blockers, or "None"]

---
Updated: [ISO timestamp]
Iteration: [current iteration]
```

### Marking criteria complete in ralph_task.md

Find the criterion and change:
```markdown
- [ ] GET /health returns 200
```
To:
```markdown
- [x] GET /health returns 200
```

## Philosophy Reminder

- **Progress persists** in files
- **Failures evaporate** with context rotation
- **Same mistake never happens twice** (guardrails)
- **You reconstruct reality from files**, not from conversation memory
- **The files are always right** - when in doubt, read them
