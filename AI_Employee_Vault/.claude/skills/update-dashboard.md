---
name: update-dashboard
description: Update Dashboard.md with current system status and pending tasks
---

# Update Dashboard Skill

This skill updates the Dashboard.md file with current system status, pending tasks, and recent activity.

## Usage

```bash
/update-dashboard
```

## Implementation

```python
import sys
from pathlib import Path

# Add agent_skills to path
vault_path = Path.cwd()
sys.path.insert(0, str(vault_path / "agent_skills"))

from task_reader import TaskReader
from dashboard_updater import DashboardUpdater

# Initialize
reader = TaskReader(str(vault_path))
dashboard = DashboardUpdater(str(vault_path))

# Get current tasks
tasks = reader.read_all_tasks()

print("Updating dashboard...")
print(f"  Pending tasks: {len(tasks)}")

# Count files in each folder
needs_action = len(list((vault_path / "Needs_Action").glob("*.md")))
plans = len(list((vault_path / "Plans").glob("*.md")))
done = len(list((vault_path / "Done").glob("*.md")))
pending_approval = len(list((vault_path / "Pending_Approval").glob("*.md")))

print(f"  Plans generated: {plans}")
print(f"  Completed: {done}")
print(f"  Pending approval: {pending_approval}")

# Update dashboard
dashboard.update_dashboard("Dashboard refreshed")

print("\n✅ Dashboard updated successfully")
```
