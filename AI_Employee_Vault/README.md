# Bronze Tier AI Employee - Complete System

## Overview

This is a **Bronze Tier Personal AI Employee** system built according to 2026 Panaverse specifications. It provides minimal viable autonomous task processing with local-first architecture.

## Features

- **Autonomous Task Detection** - File system monitoring with configurable intervals
- **Intelligent Plan Generation** - Context-aware plans with approval routing
- **Human-in-the-Loop** - Automatic approval routing for high-priority/sensitive tasks
- **Complete Audit Trail** - All actions logged to timestamped JSON files
- **Real-time Dashboard** - Live status updates in Obsidian
- **Modular Architecture** - Reusable Python modules and Claude Code skills
- **Zero Dependencies** - Uses only Python standard library

## Vault Structure

```
AI_Employee_Vault/
├── .claude/
│   └── skills/
│       ├── process-tasks.md
│       ├── update-dashboard.md
│       ├── create-task.md
│       ├── complete-task.md
│       └── audit-system.md
├── agent_skills/
│   ├── __init__.py
│   ├── task_reader.py
│   ├── plan_creator.py
│   ├── logger.py
│   └── dashboard_updater.py
├── Inbox/              # New tasks arrive here
├── Needs_Action/       # Tasks ready for processing
├── Plans/              # Generated execution plans
├── Done/               # Completed tasks archive
├── Pending_Approval/   # Human review queue
├── Logs/               # Daily JSON logs
├── Dashboard.md        # Real-time status dashboard
├── Company_Handbook.md # Rules and guidelines
└── watcher.py          # Automated task monitoring
```

## Quick Start

### 1. Install Python

```bash
# Ensure Python 3.8+
python --version
```

### 2. Run the Watcher

```bash
cd AI_Employee_Vault
python watcher.py
```

Optional: Custom check interval (in seconds)
```bash
python watcher.py 30  # Check every 30 seconds
```

### 3. Add Tasks

Drop task files into `/Inbox`:

```markdown
---
type: email
from: user@example.com
subject: "Your task subject"
received: 2026-04-08T00:00:00Z
priority: high
status: pending
---

Task description goes here.
```

## Claude Code Skills

Use these commands in Claude Code:

```bash
/process-tasks      # Process all pending tasks
/update-dashboard   # Update dashboard status
/create-task        # Create new task interactively
/complete-task      # Mark task as complete
/audit-system       # Run system health check
```

## Task Workflow

1. **New Task** → Arrives in `/Inbox` or `/Needs_Action`
2. **Watcher Detects** → Processes task automatically
3. **Plan Generated** → Creates plan in `/Plans`
4. **Approval Check** → High priority/sensitive tasks → `/Pending_Approval`
5. **Execution** → (Manual for Bronze Tier)
6. **Completion** → Move to `/Done`

## Approval Rules

Tasks require human approval if:
- Priority is `high`
- Type is `email`
- Contains sensitive keywords: invoice, payment, financial, delete, remove

## Bronze Tier Scope

### Included ✅
- Local file system monitoring
- Task detection and processing
- Intelligent plan generation
- Dashboard updates
- Audit logging
- Human-in-the-loop approval
- Claude Code integration
- Agent Skills (Python + Claude Code)

### Not Included (Silver/Gold Tier) ❌
- Gmail integration (Silver Tier)
- WhatsApp integration (Silver Tier)
- Automated task execution (Silver Tier)
- MCP servers (Silver Tier)
- Database storage (Gold Tier)
- Web dashboard (Gold Tier)

## Requirements Met

✅ Obsidian vault with Dashboard.md and Company_Handbook.md  
✅ One working Watcher script (file system monitoring)  
✅ Claude Code successfully reading from and writing to the vault  
✅ Basic folder structure: /Inbox, /Needs_Action, /Done  
✅ All AI functionality implemented as Agent Skills

## Troubleshooting

**Watcher not detecting tasks:**
- Ensure tasks have `.md` extension
- Check file permissions
- Verify vault path is correct

**Plans not generating:**
- Check task file has valid YAML frontmatter
- Ensure `/Plans` folder exists
- Review logs in `/Logs`

**Dashboard not updating:**
- Run `python agent_skills/dashboard_updater.py` manually
- Check write permissions on `Dashboard.md`

---

**Version**: 1.0.0  
**Tier**: Bronze  
**Last Updated**: 2026-04-08
