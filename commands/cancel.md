---
description: Stop the Ralph Loop and optionally clean up state
---

# Cancel Ralph Loop

The user wants to stop the Ralph Loop. Use AskUserQuestion to confirm their intent.

## Confirmation

Ask the user:
"Are you sure you want to cancel the Ralph Loop?"

Options:
1. **"Yes, keep .ralph/ files"** - Stop the loop but preserve all state for later
2. **"Yes, delete .ralph/ files"** - Stop and clean up completely (removes all progress)
3. **"No, continue working"** - Cancel the cancellation, resume the task

## Actions Based on Choice

### Option 1: Keep Files

Output:
```
Ralph Loop stopped. State files preserved in .ralph/

You can resume anytime by running:
/ralph-loop:start

Current progress:
- Iteration: [N]
- Criteria completed: [X]/[Y]
- Guardrails saved: [Z]
```

### Option 2: Delete Files

1. Remove the `.ralph/` directory entirely
2. Output:
```
Ralph Loop cancelled. All state files deleted.

The following were removed:
- ralph_task.md (task definition)
- progress.md (progress tracking)
- guardrails.md (learned constraints)
- errors.log (error history)
- activity.log (activity tracking)

To start a new Ralph Loop, run:
/ralph-loop:start
```

### Option 3: Continue Working

Output:
```
Cancellation aborted. Continuing Ralph Loop.

Current status:
[show brief status from /ralph-loop:status]
```

## Safety Note

Warn users before deletion:
"Warning: Deleting .ralph/ files will permanently remove all progress, guardrails, and history. This cannot be undone."
