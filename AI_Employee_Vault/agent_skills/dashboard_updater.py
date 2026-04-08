"""
Dashboard Updater Skill - Bronze Tier AI Employee

Updates Dashboard.md with current system status.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class DashboardUpdater:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.dashboard_path = self.vault_path / "Dashboard.md"

    def update_dashboard(self, activity_message: str = None):
        """Update the dashboard with current status."""

        # Count tasks in each folder
        needs_action_count = self.count_files("Needs_Action")
        plans_count = self.count_files("Plans")
        done_count = self.count_files("Done")
        pending_approval_count = self.count_files("Pending_Approval")

        # Get pending tasks list
        pending_tasks = self.get_pending_tasks()

        # Get recent activity
        recent_activity = self.get_recent_activity()

        # Add new activity if provided
        if activity_message:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
            recent_activity.insert(0, f"- **{timestamp}** - {activity_message}")
            # Keep only last 10 activities
            recent_activity = recent_activity[:10]

        # Generate dashboard content
        dashboard_content = self.generate_dashboard_content(
            pending_tasks,
            recent_activity,
            needs_action_count,
            plans_count,
            done_count,
            pending_approval_count
        )

        # Write to dashboard
        with open(self.dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_content)

        print("[DASHBOARD] Updated")

    def count_files(self, folder_name: str) -> int:
        """Count markdown files in a folder."""
        folder_path = self.vault_path / folder_name
        if not folder_path.exists():
            return 0
        return len(list(folder_path.glob("*.md")))

    def get_pending_tasks(self) -> List[str]:
        """Get list of pending tasks."""
        needs_action_folder = self.vault_path / "Needs_Action"
        tasks = []

        if needs_action_folder.exists():
            for task_file in needs_action_folder.glob("*.md"):
                # Read first line or frontmatter for subject
                try:
                    with open(task_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Try to extract subject from frontmatter
                        if 'subject:' in content:
                            for line in content.split('\n'):
                                if line.strip().startswith('subject:'):
                                    subject = line.split(':', 1)[1].strip().strip('"')
                                    tasks.append(f"- **{task_file.stem}**: {subject}")
                                    break
                        else:
                            tasks.append(f"- **{task_file.stem}**: Pending task")
                except:
                    tasks.append(f"- **{task_file.stem}**: Pending task")

        return tasks if tasks else ["No tasks currently pending."]

    def get_recent_activity(self) -> List[str]:
        """Get recent activity from existing dashboard."""
        if not self.dashboard_path.exists():
            return []

        try:
            with open(self.dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract activity section
            if "## Recent Activity" in content:
                activity_section = content.split("## Recent Activity")[1].split("---")[0]
                activities = [line.strip() for line in activity_section.split('\n') if line.strip().startswith('-')]
                return activities[:10]  # Keep last 10
        except:
            pass

        return []

    def generate_dashboard_content(
        self,
        pending_tasks: List[str],
        recent_activity: List[str],
        needs_action_count: int,
        plans_count: int,
        done_count: int,
        pending_approval_count: int
    ) -> str:
        """Generate dashboard markdown content."""

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # Determine status
        if needs_action_count > 0:
            status = "⚙️ Processing"
        else:
            status = "✅ Ready"

        dashboard = f"""# AI Employee Dashboard

Welcome to AI Employee Dashboard. All tasks and plans will appear here.

---

## Pending Tasks

{chr(10).join(pending_tasks)}

---

## Recent Activity

{chr(10).join(recent_activity) if recent_activity else '- No recent activity'}

---

## System Status

- **Status**: {status}
- **Last Updated**: {timestamp} UTC
- **Tasks in Queue**: {needs_action_count}
- **Plans Generated**: {plans_count}
- **Pending Approval**: {pending_approval_count}
- **Completed Tasks**: {done_count}
"""

        return dashboard


# Example usage
if __name__ == "__main__":
    vault_path = Path(__file__).parent.parent
    dashboard = DashboardUpdater(str(vault_path))

    print("=== Updating Dashboard ===")
    dashboard.update_dashboard("System initialized")
    print("Dashboard updated successfully!")
