---
description: Explain Ralph Loop and available commands
---

# Ralph Loop Help

Display comprehensive help about Ralph Loop.

## Output

```
=== Ralph Loop - Context Pollution Prevention ===

Ralph Loop is a technique for preventing context pollution in long-running
AI coding sessions. Instead of letting sessions accumulate "rot", Ralph
deliberately rotates contexts while persisting state to files.

THE PROBLEM
-----------
AI sessions accumulate "context pollution" over time:
- Repeating itself
- Undoing its own fixes
- Circular reasoning
- Confidently going in the wrong direction

Once context is polluted, adding more instructions doesn't help.
The ball is in the gutter - adding spin won't save it.

THE SOLUTION
------------
Ralph treats context pollution as a CERTAINTY, not an accident:
- Progress persists in .ralph/ files
- Failures evaporate with each rotation
- Guardrails prevent repeating the same mistake
- Fresh contexts reconstruct reality from files

COMMANDS
--------
/ralph-loop:start    Initialize or resume a Ralph task
                     - Creates .ralph/ state files for new tasks
                     - Resumes from saved state if .ralph/ exists
                     - Uses interactive planning to define success criteria

/ralph-loop:status   Show current progress
                     - Displays task overview and completion status
                     - Shows current phase and blockers
                     - Lists active guardrails

/ralph-loop:rotate   Manually trigger rotation (fresh context)
                     - Saves current progress
                     - Increments iteration counter
                     - Instructs to start new session

/ralph-loop:sign     Add a guardrail manually
                     Usage: /ralph-loop:sign <constraint text>
                     Example: /ralph-loop:sign Always run tests before committing

/ralph-loop:cancel   Stop the loop
                     - Option to keep or delete .ralph/ files
                     - Preserves progress for later if kept

/ralph-loop:help     Show this help message

STATE FILES (.ralph/)
---------------------
ralph_task.md   The anchor file - task definition + success criteria
guardrails.md   Learned constraints to prevent repeating mistakes
progress.md     Current phase, completed work, what's next
errors.log      Error history and rotation triggers
activity.log    Tool usage tracking

AUTOMATIC ROTATION
------------------
Ralph automatically triggers rotation when:
- Same error occurs 3 times (extracts guardrail first)

When rotation triggers:
1. A guardrail is extracted from the error pattern
2. Current progress is saved
3. You're instructed to start a new session
4. New session picks up from saved state

THE PHILOSOPHY
--------------
"Ralph works because it treats AI like a volatile process,
not a reliable collaborator. Your progress should persist.
Your failures should evaporate."

- Context is memory: malloc() exists, free() doesn't
- State lives in files, not in the conversation
- Guardrails are append-only: mistakes evaporate, lessons accumulate
- When confused, read the files - they are truth

WHEN TO USE RALPH
-----------------
Use Ralph when:
- Specs are crisp and success is verifiable
- Work is bulk execution (CRUD, migrations, refactors)
- You can define "done" as checkboxes
- Tasks run longer than ~30 minutes

Don't use Ralph when:
- You're still deciding what to build
- Taste and judgment matter more than correctness
- You can't define what "done" means

"If you can't write checkboxes, you're not ready to loop.
You're ready to think."
```
