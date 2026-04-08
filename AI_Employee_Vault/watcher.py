"""
Watcher Script - Bronze Tier AI Employee

Monitors /Inbox and /Needs_Action folders for new tasks.
Automatically triggers Plan Creator when new tasks are detected.
"""

import time
from pathlib import Path
import sys

# Add agent_skills to path
sys.path.insert(0, str(Path(__file__).parent / "agent_skills"))

from task_reader import TaskReader
from plan_creator import PlanCreator
from logger import Logger
from dashboard_updater import DashboardUpdater


class TaskWatcher:
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval

        # Initialize skills
        self.task_reader = TaskReader(str(self.vault_path))
        self.plan_creator = PlanCreator(str(self.vault_path))
        self.logger = Logger(str(self.vault_path))
        self.dashboard_updater = DashboardUpdater(str(self.vault_path))

        # Track processed tasks
        self.processed_tasks = set()

        # Folders to watch
        self.needs_action_folder = self.vault_path / "Needs_Action"
        self.inbox_folder = self.vault_path / "Inbox"

    def start(self):
        """Start watching for new tasks."""
        print("=" * 60)
        print("AI Employee Watcher Started")
        print("=" * 60)
        print(f"Vault Path: {self.vault_path}")
        print(f"Check Interval: {self.check_interval} seconds")
        print(f"Watching folders:")
        print(f"  - {self.needs_action_folder}")
        print(f"  - {self.inbox_folder}")
        print("\nPress Ctrl+C to stop\n")

        self.logger.log("watcher_started", details={
            "vault_path": str(self.vault_path),
            "check_interval": self.check_interval
        })

        try:
            while True:
                self.check_for_new_tasks()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\n\n[STOP] Watcher stopped by user")
            self.logger.log("watcher_stopped")

    def check_for_new_tasks(self):
        """Check both Inbox and Needs_Action for new tasks."""
        new_tasks_found = False

        # Check Needs_Action folder
        if self.needs_action_folder.exists():
            for task_file in self.needs_action_folder.glob("*.md"):
                if task_file.name not in self.processed_tasks:
                    print(f"\n[NEW] Task detected: {task_file.name}")
                    self.process_new_task(task_file)
                    new_tasks_found = True

        # Check Inbox folder
        if self.inbox_folder.exists():
            for task_file in self.inbox_folder.glob("*.md"):
                if task_file.name not in self.processed_tasks:
                    print(f"\n[INBOX] New task: {task_file.name}")
                    # Move from Inbox to Needs_Action
                    self.move_to_needs_action(task_file)
                    self.process_new_task(self.needs_action_folder / task_file.name)
                    new_tasks_found = True

        if not new_tasks_found:
            print(".", end="", flush=True)

    def process_new_task(self, task_file: Path):
        """Process a newly detected task."""
        try:
            # Parse task
            task_data = self.task_reader.parse_task_file(task_file)

            if not task_data:
                print(f"  [WARN] Failed to parse task: {task_file.name}")
                return

            print(f"  Type: {task_data['type']}")
            print(f"  Priority: {task_data['priority']}")
            print(f"  Subject: {task_data['subject']}")

            # Log task creation
            self.logger.log_task_created(
                task_file.name,
                task_data['type'],
                task_data['priority']
            )

            # Create plan
            print(f"  Creating plan...")
            plan_path = self.plan_creator.create_plan(task_data)

            # Log plan creation
            self.logger.log_plan_created(
                task_file.name,
                Path(plan_path).name
            )

            # Update dashboard
            self.dashboard_updater.update_dashboard(
                f"New task processed: {task_file.name}"
            )

            # Mark as processed
            self.processed_tasks.add(task_file.name)

            print(f"  [OK] Task processed successfully")

        except Exception as e:
            print(f"  [ERROR] Error processing task: {e}")
            self.logger.log_error(str(e), task_file.name)

    def move_to_needs_action(self, task_file: Path):
        """Move task from Inbox to Needs_Action."""
        try:
            destination = self.needs_action_folder / task_file.name
            task_file.rename(destination)

            self.logger.log_task_moved(
                task_file.name,
                "Inbox",
                "Needs_Action"
            )

            print(f"  [MOVE] Moved to Needs_Action")
        except Exception as e:
            print(f"  [WARN] Failed to move task: {e}")


def main():
    """Main entry point for the watcher."""
    # Get vault path (parent directory of this script)
    vault_path = Path(__file__).parent

    # Default check interval: 60 seconds
    check_interval = 60

    # Allow custom interval via command line
    if len(sys.argv) > 1:
        try:
            check_interval = int(sys.argv[1])
        except ValueError:
            print(f"Invalid interval: {sys.argv[1]}, using default 60 seconds")

    # Create and start watcher
    watcher = TaskWatcher(str(vault_path), check_interval)
    watcher.start()


if __name__ == "__main__":
    main()
