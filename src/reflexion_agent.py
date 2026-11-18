"""Minimal Reflexion-style actor and self-reflection interface.

The caller supplies a text-generation function. This keeps the agent logic
independent of a specific model/runtime and makes it easy to unit-test.
"""

from typing import Callable

from atr.reflexion_memory import ReflectionMemory, build_reflection_prompt


TextGenerator = Callable[[str, int], str]


def build_actor_prompt(
    task_instruction: str,
    current_state_summary: str,
    memory_text: str,
) -> str:
    """Construct the prompt used by the actor to propose its next action."""
    return f"""You are an agent completing a research workflow.

Task:
{task_instruction}

Current state known to you:
{current_state_summary}

{memory_text}

Choose the single next action that best advances the task.
Use only the information above. Do not claim an action has been executed.
Return a concise action proposal."""


class ReflexionAgent:
    """Actor + verbal self-reflection + task-scoped episodic memory."""

    def __init__(
        self,
        generate_text: TextGenerator,
        memory: ReflectionMemory | None = None,
        max_new_tokens: int = 128,
    ) -> None:
        if max_new_tokens < 1:
            raise ValueError("max_new_tokens must be >= 1")
        self.generate_text = generate_text
        self.memory = memory or ReflectionMemory()
        self.max_new_tokens = max_new_tokens

    def act(
        self,
        task_id: str,
        task_instruction: str,
        current_state_summary: str,
    ) -> str:
        """Generate one proposed action using the task's previous reflections."""
        memory_text = self.memory.render(task_id)
        prompt = build_actor_prompt(
            task_instruction, current_state_summary, memory_text
        )
        action = self.generate_text(prompt, self.max_new_tokens).strip()
        if not action:
            raise ValueError("The text generator returned an empty action")
        return action

    def reflect(
        self,
        task_id: str,
        task_instruction: str,
        attempted_action: str,
        environment_feedback: str,
        trajectory_summary: str,
        trial: int,
    ) -> str:
        """Generate, store and return a verbal lesson from environment feedback."""
        prompt = build_reflection_prompt(
            task_instruction=task_instruction,
            attempted_action=attempted_action,
            environment_feedback=environment_feedback,
            trajectory_summary=trajectory_summary,
        )
        reflection = self.generate_text(prompt, self.max_new_tokens).strip()
        if not reflection:
            raise ValueError("The text generator returned an empty reflection")
        self.memory.add(task_id, reflection, trial)
        return reflection
