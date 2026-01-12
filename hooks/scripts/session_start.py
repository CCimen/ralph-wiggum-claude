#!/usr/bin/env python3
"""
Ralph Loop - Session Start Hook

Runs when a new Claude Code session starts.
Checks for .ralph/ directory and outputs context reminder if Ralph is active.
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime

def main():
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    ralph_dir = Path(project_dir) / '.ralph'

    # Check if Ralph Loop is active
    if not ralph_dir.exists():
        sys.exit(0)  # No Ralph session, nothing to do

    task_file = ralph_dir / 'ralph_task.md'
    progress_file = ralph_dir / 'progress.md'
    guardrails_file = ralph_dir / 'guardrails.md'

    if not task_file.exists():
        sys.exit(0)  # No task file, nothing to do

    # Read task info
    task_content = task_file.read_text()
    iteration = 1
    task_name = "Unknown task"

    for line in task_content.split('\n'):
        if line.startswith('iteration:'):
            try:
                iteration = int(line.split(':')[1].strip())
            except:
                pass
        if line.startswith('task:'):
            task_name = line.split(':', 1)[1].strip()

    # Count completed criteria
    completed = task_content.count('[x]') + task_content.count('[X]')
    total = completed + task_content.count('[ ]')

    # Count guardrails
    guardrail_count = 0
    if guardrails_file.exists():
        guardrail_content = guardrails_file.read_text()
        guardrail_count = guardrail_content.count('### Sign:')

    # Log session start
    activity_log = ralph_dir / 'activity.log'
    timestamp = datetime.utcnow().isoformat() + 'Z'
    with open(activity_log, 'a') as f:
        f.write(f'[{timestamp}] SESSION_START iteration={iteration}\n')

    # Output reminder (this will be shown to Claude)
    reminder = {
        "type": "ralph_session_reminder",
        "message": f"Ralph Loop Active - Iteration {iteration}",
        "task": task_name,
        "progress": f"{completed}/{total} criteria completed",
        "guardrails": guardrail_count,
        "instructions": [
            "Read .ralph/guardrails.md before taking any action",
            "Update .ralph/progress.md after completing steps",
            "Mark checkboxes in .ralph/ralph_task.md as you complete them"
        ]
    }

    print(json.dumps(reminder, indent=2))
    sys.exit(0)

if __name__ == '__main__':
    main()
