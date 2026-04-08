---
name: audit-system
description: Run system health check and display audit report
---

# Audit System Skill

This skill performs a comprehensive system health check and displays an audit report.

## Usage

```bash
/audit-system
```

## Implementation

```python
import sys
from pathlib import Path
from datetime import datetime
import json

# Add agent_skills to path
vault_path = Path.cwd()
sys.path.insert(0, str(vault_path / "agent_skills"))

from task_reader import TaskReader
from logger import Logger

# Initialize
reader = TaskReader(str(vault_path))
logger = Logger(str(vault_path))

print("=" * 60)
print("AI EMPLOYEE SYSTEM AUDIT")
print("=" * 60)
print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
print(f"Vault Path: {vault_path}")
print()

# Check folder structure
print("=== Folder Structure ===")
required_folders = ["Inbox", "Needs_Action", "Plans", "Done", "Pending_Approval", "Logs", "agent_skills"]
for folder in required_folders:
    folder_path = vault_path / folder
    status = "✅" if folder_path.exists() else "❌"
    print(f"{status} /{folder}")
print()

# Count files
print("=== File Counts ===")
inbox_count = len(list((vault_path / "Inbox").glob("*.md")))
needs_action_count = len(list((vault_path / "Needs_Action").glob("*.md")))
plans_count = len(list((vault_path / "Plans").glob("*.md")))
done_count = len(list((vault_path / "Done").glob("*.md")))
pending_count = len(list((vault_path / "Pending_Approval").glob("*.md")))

print(f"  Inbox: {inbox_count}")
print(f"  Needs Action: {needs_action_count}")
print(f"  Plans: {plans_count}")
print(f"  Done: {done_count}")
print(f"  Pending Approval: {pending_count}")
print()

# Check core files
print("=== Core Files ===")
core_files = ["Dashboard.md", "Company_Handbook.md", "watcher.py"]
for file in core_files:
    file_path = vault_path / file
    status = "✅" if file_path.exists() else "❌"
    print(f"{status} {file}")
print()

# Check agent skills
print("=== Agent Skills ===")
skills = ["task_reader.py", "plan_creator.py", "logger.py", "dashboard_updater.py"]
for skill in skills:
    skill_path = vault_path / "agent_skills" / skill
    status = "✅" if skill_path.exists() else "❌"
    print(f"{status} {skill}")
print()

# Check recent logs
print("=== Recent Logs ===")
today = datetime.utcnow().strftime("%Y-%m-%d")
log_file = vault_path / "Logs" / f"{today}.json"
if log_file.exists():
    with open(log_file, 'r') as f:
        logs = json.load(f)
    print(f"✅ Today's log: {len(logs)} entries")
    if logs:
        print(f"   Last action: {logs[-1]['action']} at {logs[-1]['timestamp']}")
else:
    print("⚠️  No logs for today")
print()

# Validate tasks
print("=== Task Validation ===")
tasks = reader.read_all_tasks()
print(f"Total tasks in Needs_Action: {len(tasks)}")
if tasks:
    high_priority = [t for t in tasks if t['priority'] == 'high']
    print(f"  High priority: {len(high_priority)}")
    print(f"  Medium priority: {len([t for t in tasks if t['priority'] == 'medium'])}")
    print(f"  Low priority: {len([t for t in tasks if t['priority'] == 'low'])}")
print()

# System health score
total_checks = 11 + len(required_folders) + len(core_files) + len(skills)
passed_checks = (
    sum(1 for f in required_folders if (vault_path / f).exists()) +
    sum(1 for f in core_files if (vault_path / f).exists()) +
    sum(1 for s in skills if (vault_path / "agent_skills" / s).exists()) +
    (1 if log_file.exists() else 0)
)

health_score = (passed_checks / total_checks) * 100

print("=" * 60)
print(f"SYSTEM HEALTH SCORE: {health_score:.1f}%")
print("=" * 60)

if health_score == 100:
    print("✅ All systems operational")
elif health_score >= 80:
    print("⚠️  Minor issues detected")
else:
    print("❌ Critical issues detected")

# Log audit
logger.log("system_audit", details={
    "health_score": health_score,
    "tasks_pending": len(tasks),
    "files_processed": done_count
})

print()
```
