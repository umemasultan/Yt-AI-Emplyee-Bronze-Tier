---
name: complete-task
description: Mark a task as complete and move it to /Done folder
---

# Complete Task Skill

This skill marks a task as complete by moving it from /Needs_Action to /Done folder.

## Usage

```bash
/complete-task
```

## Implementation

```python
import sys
from pathlib import Path
from datetime import datetime

# Add agent_skills to path
vault_path = Path.cwd()
sys.path.insert(0, str(vault_path / "agent_skills"))

from task_reader import TaskReader
from logger import Logger
from dashboard_updater import DashboardUpdater

# Initialize
reader = TaskReader(str(vault_path))
logger = Logger(str(vault_path))
dashboard = DashboardUpdater(str(vault_path))

# Get all tasks
tasks = reader.read_all_tasks()

if not tasks:
    print("No tasks found in /Needs_Action")
    sys.exit(0)

# Display tasks
print("=== Pending Tasks ===\n")
for i, task in enumerate(tasks, 1):
    print(f"{i}. {task['filename']}")
    print(f"   Subject: {task['subject']}")
    print(f"   Priority: {task['priority']}")
    print()

# Get user selection
selection = input("Select task number to complete (or 'q' to quit): ").strip()

if selection.lower() == 'q':
    print("Cancelled")
    sys.exit(0)

try:
    task_index = int(selection) - 1
    selected_task = tasks[task_index]
except (ValueError, IndexError):
    print("Invalid selection")
    sys.exit(1)

# Move task to Done
task_file = Path(selected_task['filepath'])
done_path = vault_path / "Done" / task_file.name
task_file.rename(done_path)

print(f"\n✅ Task moved to /Done: {task_file.name}")

# Move plan to Done if exists
plan_name = f"PLAN_{task_file.stem}.md"
plan_file = vault_path / "Plans" / plan_name
if plan_file.exists():
    plan_done_path = vault_path / "Done" / plan_name
    plan_file.rename(plan_done_path)
    print(f"✅ Plan moved to /Done: {plan_name}")

# Log completion
logger.log_task_completed(task_file.name)

# Update dashboard
dashboard.update_dashboard(f"Task completed: {task_file.name}")

print("\n✅ Task marked as complete")
```
