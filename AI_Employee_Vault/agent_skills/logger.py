"""
Logger Skill - Bronze Tier AI Employee

Logs all agent actions to /Logs folder in JSON format.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class Logger:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.logs_folder = self.vault_path / "Logs"
        self.logs_folder.mkdir(exist_ok=True)

    def log(self, action: str, task_name: str = None, details: Dict[str, Any] = None):
        """Log an action to today's log file."""

        timestamp = datetime.utcnow()
        date_str = timestamp.strftime("%Y-%m-%d")
        log_file = self.logs_folder / f"{date_str}.json"

        # Create log entry
        log_entry = {
            "timestamp": timestamp.isoformat() + 'Z',
            "action": action,
            "task_name": task_name,
            "details": details or {}
        }

        # Read existing logs
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

        # Append new log entry
        logs.append(log_entry)

        # Write back to file
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

        print(f"[LOG] {action}")

    def log_task_created(self, task_name: str, task_type: str, priority: str):
        """Log task creation."""
        self.log(
            action="task_created",
            task_name=task_name,
            details={
                "type": task_type,
                "priority": priority
            }
        )

    def log_plan_created(self, task_name: str, plan_name: str):
        """Log plan creation."""
        self.log(
            action="plan_created",
            task_name=task_name,
            details={
                "plan_file": plan_name
            }
        )

    def log_task_completed(self, task_name: str):
        """Log task completion."""
        self.log(
            action="task_completed",
            task_name=task_name
        )

    def log_task_moved(self, task_name: str, from_folder: str, to_folder: str):
        """Log task movement between folders."""
        self.log(
            action="task_moved",
            task_name=task_name,
            details={
                "from": from_folder,
                "to": to_folder
            }
        )

    def log_approval_requested(self, task_name: str, reason: str):
        """Log approval request."""
        self.log(
            action="approval_requested",
            task_name=task_name,
            details={
                "reason": reason
            }
        )

    def log_error(self, error_message: str, task_name: str = None):
        """Log an error."""
        self.log(
            action="error",
            task_name=task_name,
            details={
                "error": error_message
            }
        )

    def get_today_logs(self) -> list:
        """Get all logs for today."""
        timestamp = datetime.utcnow()
        date_str = timestamp.strftime("%Y-%m-%d")
        log_file = self.logs_folder / f"{date_str}.json"

        if not log_file.exists():
            return []

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def get_logs_by_date(self, date_str: str) -> list:
        """Get logs for a specific date (YYYY-MM-DD)."""
        log_file = self.logs_folder / f"{date_str}.json"

        if not log_file.exists():
            return []

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []


# Example usage
if __name__ == "__main__":
    vault_path = Path(__file__).parent.parent
    logger = Logger(str(vault_path))

    print("=== Testing Logger ===")

    # Test various log types
    logger.log_task_created("SAMPLE_TASK_1", "email", "high")
    logger.log_plan_created("SAMPLE_TASK_1", "PLAN_SAMPLE_TASK_1.md")
    logger.log("system_initialized", details={"version": "1.0", "tier": "bronze"})

    # Display today's logs
    print("\n=== Today's Logs ===")
    logs = logger.get_today_logs()
    for log in logs:
        print(f"{log['timestamp']} - {log['action']} - {log.get('task_name', 'N/A')}")
