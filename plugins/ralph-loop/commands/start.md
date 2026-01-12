---
description: Initialize Ralph Loop for a task with interactive planning
---

# Start Ralph Loop

You are initializing a Ralph Loop session. Ralph is a technique for preventing context pollution through deliberate rotation.

## Step 1: Check for existing state

First, check if `.ralph/` directory exists in the current project:
- If YES: Read ralph_task.md, progress.md, and guardrails.md to understand current state and resume
- If NO: This is a new task, proceed to planning

## Step 2: Interactive Planning (for new tasks)

Use the AskUserQuestion tool to clarify the task with these questions:

1. **Task Definition**: "What task would you like to accomplish? Please describe it in detail."
2. **Success Criteria**: "What specific outcomes will indicate the task is complete? (These become checkboxes)"
3. **Test Command**: "Is there a test command to verify success? (e.g., 'npm test', 'pytest', or 'none')"
4. **Constraints**: "Are there any specific constraints or requirements I should know about?"

## Step 3: Create State Files

After gathering requirements, create the `.ralph/` directory with:

1. `ralph_task.md` - The anchor file with YAML frontmatter:
   ```yaml
   ---
   task: [task description]
   test_command: "[test command or 'none']"
   created: [ISO timestamp]
   iteration: 1
   status: in_progress
   ---

   # Task: [task name]

   ## Success Criteria
   - [ ] [criterion 1]
   - [ ] [criterion 2]
   ...

   ## Context
   [Any relevant context from user]

   ## Notes
   <!-- Implementation notes go here -->
   ```

2. `guardrails.md` - Initialize with:
   ```markdown
   # Guardrails

   Learned constraints to prevent repeating mistakes. Read before every action.

   ---
   ```

3. `progress.md` - Initialize with:
   ```markdown
   # Progress

   ## Current Phase
   Phase 1: Getting Started

   ## Completed
   (none yet)

   ## In Progress
   - [ ] First success criterion

   ## Next Up
   [remaining criteria]

   ## Last Action
   Initialized Ralph Loop

   ## Blocked By
   None

   ---
   Updated: [timestamp]
   Iteration: 1
   ```

4. `errors.log` - Create empty file
5. `activity.log` - Create empty file

## Step 4: Begin Execution

Start working on the first unchecked success criterion.

**CRITICAL RULES**:
- Always read guardrails.md BEFORE taking any action
- Update progress.md AFTER completing each significant step
- Mark checkboxes [x] in ralph_task.md as you complete criteria
- If you encounter the same error 3 times, STOP and inform the user that rotation is needed

## Step 5: Resuming (if .ralph/ exists)

When resuming from existing state:
1. Read ralph_task.md to see overall progress
2. Read progress.md to understand current phase and last action
3. Read guardrails.md to know what to avoid
4. Check errors.log for recent issues
5. Continue from where progress.md indicates

## Ralph Philosophy Reminder

- **Progress persists** in files, **failures evaporate** with context
- Same mistake **never happens twice** (guardrails prevent it)
- You **reconstruct reality from files**, not memory
- When confused, **read the state files** - they are truth
