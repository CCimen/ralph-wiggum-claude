#!/usr/bin/env python3
"""
Ralph Loop - Progress Updater Hook

Tracks tool usage and updates activity log.
Runs after every tool use to maintain activity history.
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

def main():
    # Read input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    ralph_dir = Path(project_dir) / '.ralph'

    # Check if Ralph Loop is active
    if not ralph_dir.exists():
        sys.exit(0)

    tool_name = input_data.get('tool_name', 'Unknown')
    tool_input = input_data.get('tool_input', {})
    tool_output = input_data.get('tool_output', {})

    timestamp = datetime.utcnow().isoformat() + 'Z'
    iteration = get_current_iteration(ralph_dir)

    # Build activity entry
    activity_entry = f'[{timestamp}] iteration={iteration} tool={tool_name}'

    # Add relevant details based on tool type
    if tool_name == 'Read':
        file_path = tool_input.get('file_path', 'unknown')
        activity_entry += f' file="{file_path}"'

    elif tool_name == 'Write':
        file_path = tool_input.get('file_path', 'unknown')
        activity_entry += f' file="{file_path}" action=create'

    elif tool_name == 'Edit':
        file_path = tool_input.get('file_path', 'unknown')
        activity_entry += f' file="{file_path}" action=edit'

    elif tool_name == 'Bash':
        command = tool_input.get('command', '')[:50]
        activity_entry += f' cmd="{command}"'

    elif tool_name == 'Glob':
        pattern = tool_input.get('pattern', '')
        activity_entry += f' pattern="{pattern}"'

    elif tool_name == 'Grep':
        pattern = tool_input.get('pattern', '')[:30]
        activity_entry += f' search="{pattern}"'

    elif tool_name == 'Task':
        desc = tool_input.get('description', '')[:30]
        activity_entry += f' task="{desc}"'

    # Check for errors
    is_error = tool_output.get('is_error', False)
    if is_error:
        activity_entry += ' status=ERROR'
    else:
        activity_entry += ' status=OK'

    activity_entry += '\n'

    # Append to activity log
    activity_log = ralph_dir / 'activity.log'
    with open(activity_log, 'a') as f:
        f.write(activity_entry)

    sys.exit(0)

if __name__ == '__main__':
    main()
