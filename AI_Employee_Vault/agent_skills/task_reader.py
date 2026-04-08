"""
Task Reader Skill - Bronze Tier AI Employee

Reads all task files from /Needs_Action folder and extracts metadata.
"""

import os
from pathlib import Path
from typing import List, Dict
import re
from datetime import datetime


class TaskReader:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action_folder = self.vault_path / "Needs_Action"

    def read_all_tasks(self) -> List[Dict]:
        """Read all task files and extract metadata."""
        tasks = []

        if not self.needs_action_folder.exists():
            print(f"Warning: {self.needs_action_folder} does not exist")
            return tasks

        for task_file in self.needs_action_folder.glob("*.md"):
            task_data = self.parse_task_file(task_file)
            if task_data:
                tasks.append(task_data)

        return tasks

    def parse_task_file(self, file_path: Path) -> Dict:
        """Parse a single task file and extract metadata."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter metadata
            metadata = self.extract_frontmatter(content)

            # Extract body content (after frontmatter)
            body = self.extract_body(content)

            task_data = {
                'filename': file_path.name,
                'filepath': str(file_path),
                'type': metadata.get('type', 'unknown'),
                'from': metadata.get('from', ''),
                'subject': metadata.get('subject', ''),
                'received': metadata.get('received', ''),
                'priority': metadata.get('priority', 'medium'),
                'status': metadata.get('status', 'pending'),
                'body': body,
                'metadata': metadata
            }

            return task_data

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def extract_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from markdown content."""
        metadata = {}

        # Match frontmatter between --- markers
        frontmatter_pattern = r'^---\s*\n(.*?)\n---'
        match = re.search(frontmatter_pattern, content, re.DOTALL | re.MULTILINE)

        if match:
            frontmatter = match.group(1)
            # Parse simple key: value pairs
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"')

        return metadata

    def extract_body(self, content: str) -> str:
        """Extract body content after frontmatter."""
        # Remove frontmatter
        frontmatter_pattern = r'^---\s*\n.*?\n---\s*\n'
        body = re.sub(frontmatter_pattern, '', content, flags=re.DOTALL | re.MULTILINE)
        return body.strip()

    def get_tasks_by_priority(self, priority: str) -> List[Dict]:
        """Get all tasks with specific priority."""
        all_tasks = self.read_all_tasks()
        return [task for task in all_tasks if task['priority'] == priority]

    def get_high_priority_tasks(self) -> List[Dict]:
        """Get all high priority tasks."""
        return self.get_tasks_by_priority('high')


# Example usage
if __name__ == "__main__":
    vault_path = Path(__file__).parent.parent
    reader = TaskReader(str(vault_path))

    print("=== Reading All Tasks ===")
    tasks = reader.read_all_tasks()

    for task in tasks:
        print(f"\nTask: {task['filename']}")
        print(f"  Type: {task['type']}")
        print(f"  From: {task['from']}")
        print(f"  Subject: {task['subject']}")
        print(f"  Priority: {task['priority']}")
        print(f"  Status: {task['status']}")
