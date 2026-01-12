---
description: "Show Ralph Loop documentation: what it is, how it works, all available commands, state files, and when to use it vs regular sessions."
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
/ralph-loop:start    Start or resume a Ralph Loop task
                     - NEW TASK: Creates .ralph/ files, asks for task definition,
                       success criteria, test command, and max iterations (default: 50)
                     - RESUME: Reads existing .ralph/ state and continues work
                     - AUTO-STOPS when max iterations reached

/ralph-loop:status   Show where you are in the loop
                     - Task: what you're doing + which iteration you're on
                     - Progress: X/Y checkboxes completed
                     - Guardrails: learned constraints being enforced
                     - Blockers: what's preventing progress

/ralph-loop:rotate   Force a fresh context (manual rotation)
                     - USE WHEN: AI is stuck, repeating itself, going in circles
                     - Saves all progress to .ralph/ files
                     - Increments iteration counter
                     - Tells you to exit Claude and start a new session
                     - New session picks up exactly where you left off

/ralph-loop:sign     Add a rule to prevent a mistake from recurring
                     Usage: /ralph-loop:sign <rule text>
                     Example: /ralph-loop:sign Always run tests before committing
                     Example: /ralph-loop:sign Check for null before accessing .length

/ralph-loop:cancel   Stop the Ralph Loop (the only way to end it manually)
                     - "Keep files": stops loop, preserves .ralph/ for later
                     - "Delete files": stops loop, removes all progress
                     - Loop also auto-stops when max iterations reached

/ralph-loop:help     Show this help message

STATE FILES (.ralph/)
---------------------
ralph_task.md   The anchor file - task definition + success criteria
guardrails.md   Learned constraints to prevent repeating mistakes
progress.md     Current phase, completed work, what's next
errors.log      Error history and rotation triggers
activity.log    Tool usage tracking

HOW THE LOOP STOPS
------------------
There are THREE ways a Ralph Loop ends:

1. TASK COMPLETE: All success criteria checkboxes are marked [x]
   - The natural end state - you're done!

2. MAX ITERATIONS REACHED: Loop auto-stops at the limit (default: 50)
   - Prevents runaway loops that never complete
   - You can resume with /ralph-loop:start and set a higher limit

3. MANUAL CANCEL: You run /ralph-loop:cancel
   - Choose to keep .ralph/ files (resume later) or delete them

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
