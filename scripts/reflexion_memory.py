"""Minimal task-scoped verbal reflection memory for the ATR B2 baseline.

This module stores LLM-generated reflections. It does not generate reflections,
inspect authoritative environment state, or modify agent beliefs.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Reflection:
    """One verbal lesson produced after receiving task feedback."""

    task_id: str
    text: str
    trial: int


class ReflectionMemory:
    """Store and retrieve recent reflections separately for each task."""

    def __init__(self, max_items_per_task: int = 3) -> None:
        if max_items_per_task < 1:
            raise ValueError("max_items_per_task must be at least 1")
        self.max_items_per_task = max_items_per_task
        self._items: Dict[str, List[Reflection]] = {}

    def add(self, task_id: str, text: str, trial: int) -> None:
        """Append a non-empty reflection and retain only the most recent items."""
        if not task_id.strip():
            raise ValueError("task_id cannot be empty")
        if not text.strip():
            raise ValueError("reflection text cannot be empty")
        if trial < 1:
            raise ValueError("trial must be >= 1")

        items = self._items.setdefault(task_id, [])
        items.append(Reflection(task_id=task_id, text=text.strip(), trial=trial))
        self._items[task_id] = items[-self.max_items_per_task :]

    def recall(self, task_id: str) -> List[Reflection]:
        """Return a copy of the stored reflections, oldest to newest."""
        return list(self._items.get(task_id, []))

    def render(self, task_id: str) -> str:
        """Format task-specific lessons for inclusion in the next actor prompt."""
        items = self.recall(task_id)
        if not items:
            return "No previous reflections are available for this task."

        lines = ["Lessons from previous attempts on this task:"]
        for item in items:
            lines.append(f"- Trial {item.trial}: {item.text}")
        return "\n".join(lines)


def build_reflection_prompt(
    task_instruction: str,
    attempted_action: str,
    environment_feedback: str,
    trajectory_summary: str,
) -> str:
    """Build the self-reflection request; an LLM must produce the actual lesson."""
    return f"""You are reviewing an attempted research-workflow action.

Task:
{task_instruction}

Recent trajectory:
{trajectory_summary}

Attempted action:
{attempted_action}

Feedback from the environment:
{environment_feedback}

Write a concise, evidence-based lesson for the next attempt. Identify what
assumption or decision led to the problem and state what should be checked or
done differently. Do not claim access to hidden state. Do not invent facts.
Return only the reflection text; do not choose the next action."""
