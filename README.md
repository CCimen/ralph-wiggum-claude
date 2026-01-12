# Ralph Loop Plugin for Claude Code

A Claude Code plugin that implements the **Ralph Wiggum technique** for context pollution prevention. Instead of letting AI sessions accumulate "rot" (repetitive errors, circular reasoning, undoing fixes), Ralph deliberately rotates contexts while persisting state to files.

## The Problem

AI coding sessions accumulate "context pollution" over time:
- Repeating itself
- Undoing its own fixes
- Circular reasoning
- Confidently going in the wrong direction

Once context is polluted, adding more instructions doesn't help. **The ball is in the gutter - adding spin won't save it.**

## The Solution

Ralph treats context pollution as a **certainty**, not an accident:
- **Progress persists** in `.ralph/` files
- **Failures evaporate** with each rotation
- **Guardrails** prevent repeating the same mistake
- Fresh contexts **reconstruct reality from files**

## Installation

### Option 1: Local Development

```bash
# Clone the repository
git clone https://github.com/CCimen/ralph-wiggum-claude.git

# Use with --plugin-dir flag
claude --plugin-dir /path/to/ralph-wiggum-claude
```

### Option 2: Add to Claude Code Plugins (when marketplace available)

```bash
/plugin install ralph-loop
```

## Quick Start

1. **Start a Ralph Loop session:**
   ```
   /ralph-loop:start
   ```
   This will interactively gather your task definition and success criteria.

2. **Check progress anytime:**
   ```
   /ralph-loop:status
   ```

3. **Add constraints manually:**
   ```
   /ralph-loop:sign Always run tests before committing
   ```

4. **Trigger rotation when stuck:**
   ```
   /ralph-loop:rotate
   ```

5. **Get help:**
   ```
   /ralph-loop:help
   ```

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-loop:start` | Initialize or resume a Ralph task |
| `/ralph-loop:status` | Show current progress |
| `/ralph-loop:rotate` | Manually trigger rotation (fresh context) |
| `/ralph-loop:sign <text>` | Add a guardrail manually |
| `/ralph-loop:cancel` | Stop the loop |
| `/ralph-loop:help` | Show help |

## State Files

Ralph persists state in a `.ralph/` directory in your project:

| File | Purpose |
|------|---------|
| `ralph_task.md` | Anchor file - task definition + success criteria checkboxes |
| `guardrails.md` | Learned constraints to prevent repeating mistakes |
| `progress.md` | Current phase, completed work, what's next |
| `errors.log` | Error history and rotation triggers |
| `activity.log` | Tool usage tracking |

## How Rotation Works

### Automatic Rotation

Ralph automatically triggers rotation when:
- **Same error occurs 3 times** - A guardrail is extracted first

When triggered:
1. A guardrail is extracted from the error pattern
2. Current progress is saved
3. You're instructed to start a new Claude Code session
4. New session picks up from saved state

### Manual Rotation

Use `/ralph-loop:rotate` when you notice:
- Circular reasoning patterns
- Undoing previous changes
- Increasing confusion
- Progress has stalled

## Guardrails

Guardrails are learned constraints that prevent repeating mistakes.

**Auto-extracted** when errors repeat:
```markdown
### Sign: Always run 'npm install' after adding dependencies
- Trigger: npm ERR! Cannot find module 'xyz'
- Added: Iteration 2 (auto)
```

**Manually added** via `/ralph-loop:sign`:
```markdown
### Sign: Use async/await instead of callbacks
- Trigger: User-added constraint
- Added: Iteration 1 (manual)
```

Guardrails are **append-only**: mistakes evaporate, lessons accumulate.

## When to Use Ralph

**Use Ralph when:**
- Specs are crisp and success is verifiable
- Work is bulk execution (CRUD, migrations, refactors, porting)
- You can define "done" as checkboxes
- Tasks run longer than ~30 minutes

**Don't use Ralph when:**
- You're still deciding what to build
- Taste and judgment matter more than correctness
- You can't define what "done" means

> "If you can't write checkboxes, you're not ready to loop. You're ready to think."

## Philosophy

Ralph works because it treats AI like a **volatile process**, not a reliable collaborator.

- **Context is memory**: `malloc()` exists, `free()` doesn't
- **State lives in files**, not in the conversation
- **Guardrails are append-only**: mistakes evaporate, lessons accumulate
- **When confused, read the files** - they are truth

> "Your progress should persist. Your failures should evaporate."

## Credits

Based on the Ralph Wiggum technique coined and popularized by [@GeoffreyHuntley](https://twitter.com/GeoffreyHuntley).

Cursor implementation inspiration from [@agrimsingh](https://twitter.com/agrimsingh).

## License

MIT License - See [LICENSE](LICENSE) for details.

## Author

CCimen
