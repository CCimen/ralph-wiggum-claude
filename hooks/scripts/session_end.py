#!/usr/bin/env python3
"""
Ralph Loop - Session End Hook

Runs when Claude Code session ends.
Updates progress file with session summary.
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

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

def count_session_activity(ralph_dir: Path, iteration: int) -> dict:
    """Count activity from current iteration."""
    activity_log = ralph_dir / 'activity.log'
    if not activity_log.exists():
        return {'tools': 0, 'errors': 0}

    tools = 0
    errors = 0

    with open(activity_log, 'r') as f:
        for line in f:
            if f'iteration={iteration}' in line:
                tools += 1
                if 'status=ERROR' in line:
                    errors += 1

    return {'tools': tools, 'errors': errors}

def main():
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    ralph_dir = Path(project_dir) / '.ralph'

    # Check if Ralph Loop is active
    if not ralph_dir.exists():
        sys.exit(0)

    timestamp = datetime.utcnow().isoformat() + 'Z'
    iteration = get_current_iteration(ralph_dir)
    activity = count_session_activity(ralph_dir, iteration)

    # Log session end
    activity_log = ralph_dir / 'activity.log'
    with open(activity_log, 'a') as f:
        f.write(f'[{timestamp}] SESSION_END iteration={iteration} tools={activity["tools"]} errors={activity["errors"]}\n')

    # Update progress.md timestamp
    progress_file = ralph_dir / 'progress.md'
    if progress_file.exists():
        content = progress_file.read_text()

        # Update the timestamp at the bottom
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('Updated:'):
                new_lines.append(f'Updated: {timestamp}')
            else:
                new_lines.append(line)

        progress_file.write_text('\n'.join(new_lines))

    sys.exit(0)

if __name__ == '__main__':
    main()
