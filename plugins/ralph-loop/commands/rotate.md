---
description: "Force a context rotation when you notice the AI is stuck, repeating itself, or going in circles. Saves progress, then instructs you to start a new Claude session. The new session picks up where this one left off."
---

# Manual Ralph Rotation

The user is manually triggering a rotation to get a fresh context. This is useful when:
- You notice circular reasoning patterns
- The AI keeps undoing its own changes
- Progress has stalled despite multiple attempts
- You want to start fresh while keeping progress

## Rotation Steps

### 1. Check Max Iterations First

Read `.ralph/ralph_task.md` and check:
- Current `iteration` value
- `max_iterations` limit (default: 50)

If `iteration + 1 >= max_iterations`:
- Set status to "auto_stopped"
- Output: "Ralph Loop reached max iterations ([N]/[max]). Loop auto-stopped. Use /ralph-loop:start to continue with a higher limit."
- DO NOT proceed with rotation

### 2. Update Iteration Counter

Increment the iteration number in the frontmatter:
```yaml
iteration: [current + 1]
```

### 3. Save Current Progress

Update `.ralph/progress.md` with:
- Current timestamp
- New iteration number
- Summary of what was accomplished this iteration
- What should be tackled next iteration

### 4. Log the Rotation

Append to `.ralph/errors.log`:
```
[timestamp] ROTATION_TRIGGERED reason="manual" iteration=[N]
```

### 5. Inform the User

Output this message:

```
Ralph rotation triggered. Current progress has been saved.

Iteration [N] -> [N+1]
Progress preserved in .ralph/

To continue with fresh context:
1. Start a new Claude Code session (exit and restart)
2. Run /ralph-loop:start to resume from saved state

Why rotate?
- Fresh context = no accumulated confusion
- Guardrails prevent repeating mistakes
- Progress is preserved in files
- The new session reconstructs reality from .ralph/ files
```

## Important Notes

- DO NOT continue working after triggering rotation
- The whole point is to get a FRESH context
- Instruct user to start a new session
- All progress is preserved in .ralph/ directory
