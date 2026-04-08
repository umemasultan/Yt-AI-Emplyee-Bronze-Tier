# Claude Code Agent Skills - Bronze Tier

This directory contains Claude Code agent skills that can be invoked directly in Claude Code CLI.

## Available Skills

### 1. `/process-tasks`
Process all pending tasks in /Needs_Action and create execution plans.

**Usage:**
```bash
/process-tasks
```

**What it does:**
- Reads all tasks from /Needs_Action
- Creates execution plans for each task
- Logs all actions
- Updates dashboard

---

### 2. `/update-dashboard`
Update Dashboard.md with current system status.

**Usage:**
```bash
/update-dashboard
```

**What it does:**
- Counts tasks in all folders
- Gets recent activity from logs
- Updates Dashboard.md with fresh data

---

### 3. `/create-task`
Create a new task interactively.

**Usage:**
```bash
/create-task
```

**What it does:**
- Prompts for task details (type, subject, priority, description)
- Creates task file in /Inbox
- Logs the action
- Updates dashboard

---

### 4. `/complete-task`
Mark a task as complete and move it to /Done.

**Usage:**
```bash
/complete-task
```

**What it does:**
- Lists all pending tasks
- Prompts user to select task
- Moves task and plan to /Done
- Logs completion
- Updates dashboard

---

### 5. `/audit-system`
Run comprehensive system health check.

**Usage:**
```bash
/audit-system
```

**What it does:**
- Checks folder structure integrity
- Counts files in each folder
- Validates task files
- Checks recent logs
- Displays health score

---

## How Skills Work

These skills are markdown files that contain Python code. When you invoke a skill in Claude Code:

1. Claude Code reads the skill file
2. Executes the Python code in the implementation section
3. Returns the output to you

## Requirements

- Python 3.8+
- All agent_skills modules (task_reader.py, plan_creator.py, logger.py, dashboard_updater.py)
- Proper vault folder structure

## Testing Skills

You can test each skill by running:

```bash
cd AI_Employee_Vault
# Then in Claude Code CLI:
/process-tasks
/update-dashboard
/create-task
/complete-task
/audit-system
```

---

**Created:** 2026-04-08  
**Version:** 1.0.0  
**Tier:** Bronze
