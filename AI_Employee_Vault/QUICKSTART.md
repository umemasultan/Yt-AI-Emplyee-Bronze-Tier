# Bronze Tier - Quick Start Guide

## Setup (5 minutes)

### 1. Prerequisites
- Python 3.8 or higher
- Obsidian (optional, for viewing vault)
- Git (for version control)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/umemasultan/Yt-AI-Emplyee-Bronze-Tier.git
cd Yt-AI-Emplyee-Bronze-Tier/AI_Employee_Vault

# No dependencies to install - uses Python standard library only!
```

### 3. Start the Watcher

```bash
python watcher.py
```

The watcher will start monitoring for new tasks.

---

## Usage

### Adding a Task

Create a markdown file in `/Inbox`:

```markdown
---
type: email
from: user@example.com
subject: "Task subject"
priority: medium
status: pending
---

Task description here.
```

The watcher will automatically:
1. Detect the new task
2. Move it to /Needs_Action
3. Generate an execution plan
4. Update the dashboard

### Using Claude Code Skills

In Claude Code CLI:

```bash
/process-tasks      # Process all pending tasks
/update-dashboard   # Refresh dashboard
/create-task        # Create new task interactively
/complete-task      # Mark task as done
/audit-system       # Check system health
```

### Viewing the Dashboard

Open `Dashboard.md` in Obsidian or any markdown viewer to see:
- Pending tasks
- Recent activity
- System status
- Task counts

---

## Folder Structure

```
AI_Employee_Vault/
├── Inbox/              # Drop new tasks here
├── Needs_Action/       # Tasks being processed
├── Plans/              # Generated execution plans
├── Done/               # Completed tasks
├── Pending_Approval/   # Tasks requiring human review
└── Logs/               # Daily JSON logs
```

---

## Task Priority Levels

- **high** - Requires immediate attention and approval
- **medium** - Normal priority (default)
- **low** - Can be processed when time permits

---

## Approval Rules

Tasks automatically go to /Pending_Approval if:
- Priority is `high`
- Type is `email`
- Contains keywords: invoice, payment, financial, delete, remove

---

## Troubleshooting

**Watcher not starting?**
- Check Python version: `python --version`
- Ensure you're in AI_Employee_Vault directory

**Tasks not being detected?**
- Verify file has `.md` extension
- Check YAML frontmatter is valid
- Look at logs in /Logs folder

**Dashboard not updating?**
- Run `/update-dashboard` manually
- Check file permissions

---

## Next Steps

1. ✅ Test with sample task (SAMPLE_TASK_1.md included)
2. ✅ Try Claude Code skills
3. ✅ Create your own tasks
4. ✅ Monitor dashboard in Obsidian

---

**Ready to go!** 🚀
