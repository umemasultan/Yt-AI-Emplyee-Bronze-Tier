---
name: create-task
description: Create a new task in /Inbox with proper metadata
---

# Create Task Skill

This skill creates a new task file in the /Inbox folder with proper YAML frontmatter.

## Usage

```bash
/create-task
```

## Implementation

```python
import sys
from pathlib import Path
from datetime import datetime

# Add agent_skills to path
vault_path = Path.cwd()
sys.path.insert(0, str(vault_path / "agent_skills"))

from logger import Logger
from dashboard_updater import DashboardUpdater

# Initialize
logger = Logger(str(vault_path))
dashboard = DashboardUpdater(str(vault_path))

# Get task details from user
print("=== Create New Task ===\n")

task_type = input("Task type (email/message/file/other): ").strip() or "other"
subject = input("Subject: ").strip() or "New Task"
priority = input("Priority (high/medium/low): ").strip() or "medium"
from_field = input("From (email/name): ").strip() or "user"
description = input("Description: ").strip() or "Task description"

# Generate filename
timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
filename = f"TASK_{timestamp}.md"

# Create task content
content = f"""---
type: {task_type}
from: {from_field}
subject: {subject}
received: {datetime.utcnow().isoformat()}Z
priority: {priority}
status: pending
---

{description}
"""

# Save to Inbox
inbox_path = vault_path / "Inbox" / filename
inbox_path.write_text(content, encoding='utf-8')

print(f"\n✅ Task created: {filename}")
print(f"   Location: /Inbox/{filename}")

# Log action
logger.log_task_created(filename, task_type, priority)

# Update dashboard
dashboard.update_dashboard(f"New task created: {filename}")

print("\nThe watcher will automatically process this task.")
```
