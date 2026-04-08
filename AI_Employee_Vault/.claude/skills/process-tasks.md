---
name: process-tasks
description: Process all pending tasks in /Needs_Action and create execution plans
---

# Process Tasks Skill

This skill processes all pending tasks in the /Needs_Action folder and creates execution plans.

## Usage

```bash
/process-tasks
```

## Implementation

```python
import sys
from pathlib import Path

# Add agent_skills to path
vault_path = Path.cwd()
sys.path.insert(0, str(vault_path / "agent_skills"))

from task_reader import TaskReader
from plan_creator import PlanCreator
from logger import Logger
from dashboard_updater import DashboardUpdater

# Initialize skills
reader = TaskReader(str(vault_path))
plan_creator = PlanCreator(str(vault_path))
logger = Logger(str(vault_path))
dashboard = DashboardUpdater(str(vault_path))

# Read all tasks
tasks = reader.read_all_tasks()

print(f"Found {len(tasks)} tasks in /Needs_Action\n")

# Process each task
for task in tasks:
    print(f"Processing: {task['filename']}")
    print(f"  Type: {task['type']}")
    print(f"  Priority: {task['priority']}")
    print(f"  Subject: {task['subject']}")
    
    # Create plan
    plan_path = plan_creator.create_plan(task)
    print(f"  Plan created: {Path(plan_path).name}")
    
    # Log action
    logger.log_plan_created(task['filename'], Path(plan_path).name)
    
    print()

# Update dashboard
dashboard.update_dashboard(f"Processed {len(tasks)} tasks")

print(f"✅ All tasks processed successfully")
```
