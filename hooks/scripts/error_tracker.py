#!/usr/bin/env python3
"""
Ralph Loop - Error Tracker Hook

Tracks errors and detects repetition patterns.
Triggers rotation when same error occurs 3x.
Auto-extracts guardrails from repeated failures.
"""
import json
import sys
import os
import hashlib
from datetime import datetime
from pathlib import Path

ERROR_THRESHOLD = 3

def hash_error(error_msg: str) -> str:
    """Create a normalized hash of error message."""
    # Normalize: lowercase, remove timestamps, trim whitespace
    normalized = error_msg.lower().strip()
    # Remove common variable parts (line numbers, timestamps, paths)
    import re
    normalized = re.sub(r'\d+', 'N', normalized)  # Replace numbers
    normalized = re.sub(r'/[^\s]+', '/PATH', normalized)  # Replace paths
    return hashlib.md5(normalized.encode()).hexdigest()[:12]

def get_recent_errors(errors_log: Path) -> dict:
    """Count recent error occurrences by hash."""
    if not errors_log.exists():
        return {}

    errors = {}
    with open(errors_log, 'r') as f:
        for line in f:
            if 'error="' in line and 'ROTATION_TRIGGERED' not in line:
                try:
                    error_start = line.index('error="') + 7
                    error_end = line.rindex('"')
                    error_msg = line[error_start:error_end]
                    error_hash = hash_error(error_msg)
                    errors[error_hash] = {
                        'count': errors.get(error_hash, {}).get('count', 0) + 1,
                        'message': error_msg
                    }
                except ValueError:
                    continue
    return errors

def get_current_iteration(ralph_dir: Path) -> int:
    """Get current iteration from ralph_task.md"""
    task_file = ralph_dir / 'ralph_task.md'
    if task_file.exists():
        content = task_file.read_text()
        for line in content.split('\n'):
            if line.startswith('iteration:'):
                try:
                    return int(line.split(':')[1].strip())
                except:
                    pass
    return 1

def extract_guardrail(error_msg: str) -> str:
    """Extract a guardrail instruction from error message."""
    error_lower = error_msg.lower()

    # Node.js / npm patterns
    if 'cannot find module' in error_lower:
        return "Always run 'npm install' after adding dependencies to package.json"
    if 'enoent' in error_lower:
        return "Verify file/directory exists before attempting to read or modify it"
    if 'eacces' in error_lower or 'permission denied' in error_lower:
        return "Check file permissions before write operations"

    # Python patterns
    if 'modulenotfounderror' in error_lower or 'no module named' in error_lower:
        return "Ensure Python dependencies are installed before importing"
    if 'filenotfounderror' in error_lower:
        return "Verify file path exists before file operations"
    if 'indentationerror' in error_lower:
        return "Maintain consistent indentation (spaces vs tabs)"

    # Git patterns
    if 'already exists' in error_lower:
        return "Check if resource/file already exists before creating"
    if 'merge conflict' in error_lower:
        return "Resolve merge conflicts before proceeding"

    # Database patterns
    if 'duplicate key' in error_lower or 'unique constraint' in error_lower:
        return "Check for existing records before insert operations"
    if 'foreign key' in error_lower:
        return "Ensure referenced records exist before creating relationships"

    # Generic patterns
    if 'timeout' in error_lower:
        return "Add timeout handling for operations that may hang"
    if 'connection refused' in error_lower:
        return "Verify service is running before attempting connection"
    if 'syntax error' in error_lower:
        return "Validate syntax before executing code changes"

    # Default: create guardrail from error pattern
    # Truncate and clean the error for readability
    clean_error = error_msg[:80].replace('"', "'").replace('\n', ' ')
    return f"Avoid operations that cause: {clean_error}"

def add_guardrail(ralph_dir: Path, guardrail: str, trigger_error: str, iteration: int):
    """Append guardrail to guardrails.md"""
    guardrails_file = ralph_dir / 'guardrails.md'
    timestamp = datetime.utcnow().isoformat() + 'Z'

    entry = f"""
### Sign: {guardrail}
- **Trigger**: {trigger_error[:100]}
- **Added**: Iteration {iteration} ({timestamp})
"""

    with open(guardrails_file, 'a') as f:
        f.write(entry)

    # Log the guardrail addition
    errors_log = ralph_dir / 'errors.log'
    with open(errors_log, 'a') as f:
        f.write(f'[{timestamp}] GUARDRAIL_ADDED "{guardrail}" iteration={iteration}\n')

def trigger_rotation(ralph_dir: Path, error_msg: str, count: int, iteration: int):
    """Signal that rotation is needed."""
    timestamp = datetime.utcnow().isoformat() + 'Z'
    errors_log = ralph_dir / 'errors.log'

    # Log rotation trigger
    with open(errors_log, 'a') as f:
        f.write(f'[{timestamp}] ROTATION_TRIGGERED reason="error_repetition" pattern="{error_msg[:100]}" count={count}\n')

    # Extract and add guardrail
    guardrail = extract_guardrail(error_msg)
    add_guardrail(ralph_dir, guardrail, error_msg, iteration)

    # Write rotation signal file
    signal_file = ralph_dir / '.rotation_needed'
    signal_file.write_text(json.dumps({
        'reason': 'error_repetition',
        'error': error_msg[:200],
        'count': count,
        'timestamp': timestamp,
        'guardrail_added': guardrail
    }, indent=2))

    # Output message for Claude (this blocks further actions)
    print(json.dumps({
        'decision': 'block',
        'reason': f'''RALPH ROTATION NEEDED

Same error occurred {count} times. Context pollution detected.

Error pattern: {error_msg[:100]}

Guardrail added: "{guardrail}"

To continue with fresh context:
1. Start a new Claude Code session
2. Run /ralph-loop:start to resume

Your progress is preserved in .ralph/'''
    }))

    sys.exit(2)  # Exit code 2 blocks the action

def main():
    # Read input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # No valid input, skip

    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    ralph_dir = Path(project_dir) / '.ralph'

    # Check if Ralph Loop is active
    if not ralph_dir.exists():
        sys.exit(0)

    tool_name = input_data.get('tool_name', '')
    tool_output = input_data.get('tool_output', {})

    # Check if tool failed
    is_error = tool_output.get('is_error', False)
    stderr = tool_output.get('stderr', '')

    if not is_error and not stderr:
        sys.exit(0)  # No error, nothing to track

    error_msg = stderr or str(tool_output.get('content', ''))
    if not error_msg.strip():
        sys.exit(0)

    timestamp = datetime.utcnow().isoformat() + 'Z'
    iteration = get_current_iteration(ralph_dir)

    # Ensure errors.log exists
    errors_log = ralph_dir / 'errors.log'
    errors_log.touch()

    # Log the error
    with open(errors_log, 'a') as f:
        clean_error = error_msg[:200].replace('\n', ' ').replace('"', "'")
        f.write(f'[{timestamp}] iteration={iteration} tool={tool_name} error="{clean_error}"\n')

    # Check for repetition
    errors = get_recent_errors(errors_log)
    error_hash = hash_error(error_msg)

    if error_hash in errors and errors[error_hash]['count'] >= ERROR_THRESHOLD:
        trigger_rotation(ralph_dir, error_msg, errors[error_hash]['count'], iteration)

    sys.exit(0)

if __name__ == '__main__':
    main()
