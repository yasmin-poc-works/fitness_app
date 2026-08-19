from __future__ import annotations

import os
from dotenv import load_dotenv

from dataclasses import dataclass
from typing import Literal

from groq import Groq

load_dotenv()

FitnessGoal = Literal["Build muscle", "Lose fat", "General fitness", "Improve endurance"]
ExperienceLevel = Literal["Beginner", "Intermediate", "Advanced"]
EquipmentAccess = Literal["No equipment", "Home dumbbells", "Full gym"]


@dataclass(frozen=True)
class WorkoutPreferences:
    height: int
    weight: int
    fitness_goal: FitnessGoal
    experience_level: ExperienceLevel
    days_per_week: int
    mins_per_day: int
    goal_weight: int
    equipment_access: EquipmentAccess
    injuries_or_limitations: str = ""


def validate_preferences(preferences: WorkoutPreferences) -> None:
    if preferences.height < 100 or preferences.height > 250:
        raise ValueError("Height must be between 100 and 250 cm.")
    if preferences.weight < 30 or preferences.weight > 200:
        raise ValueError("Weight must be between 30 and 200 kg.")
    if preferences.mins_per_day < 15 or preferences.mins_per_day > 200:
        raise ValueError("Minutes available per day must be between 15 and 200.")
    if preferences.goal_weight < 40 or preferences.goal_weight > 200:
        raise ValueError("Goal weight must be between 40 and 200 kg.")
    if preferences.days_per_week < 1 or preferences.days_per_week > 7:
        raise ValueError("Days available per week must be between 1 and 7.")
    if not preferences.fitness_goal:
        raise ValueError("Please choose a fitness goal.")
    if not preferences.experience_level:
        raise ValueError("Please choose an experience level.")
    if not preferences.equipment_access:
        raise ValueError("Please choose an equipment option.")


def build_messages(preferences: WorkoutPreferences) -> list[dict[str, str]]:
    injury_note = ""
    if preferences.injuries_or_limitations.strip():
        injury_note = (
            "The user mentioned these injuries or limitations: "
            f"{preferences.injuries_or_limitations.strip()}.\n"
            "Include a short safety note and avoid medical claims. "
            "Offer exercise substitutions where appropriate."
        )

    system_message = (
        "You are an experienced personal trainer and fitness programmer. "
        "Create safe, practical weekly workout plans that respect the user's constraints. "
        "Return the plan in clean markdown with clear day-by-day sections, exercise lists, sets, reps, "
        "rest times, and a short warm-up. Keep the plan realistic for a real person to follow. "
        "Do not give medical advice or diagnose injuries."
    )

    user_message = f"""
Write a personalized weekly workout plan with these requirements:

- Height: {preferences.height} cm
- Weight: {preferences.weight} kg
- Fitness goal: {preferences.fitness_goal}
- Experience level: {preferences.experience_level}
- Days available per week: {preferences.days_per_week}
- Minutes available per day: {preferences.mins_per_day}
- Goal weight: {preferences.goal_weight} kg
- Equipment access: {preferences.equipment_access}
{injury_note}

Formatting rules:
- Start with a one-paragraph summary of the training split.
- Use headings like "Day 1", "Day 2", etc.
- For each training day, include warm-up, main workout, and optional finisher or mobility work.
- For each exercise, include sets and reps, or duration for cardio.
- Include rest days if there are fewer training days than days in the week.
- Keep the response concise, scannable, and specific.
- If the user has limitations, add a brief safety disclaimer at the end.
""".strip()

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]


def generate_workout_plan(
    preferences: WorkoutPreferences,
    api_key: str | None = None,
    model: str | None = None,
) -> str:
    validate_preferences(preferences)

    resolved_api_key = (api_key or os.getenv("GROQ_API_KEY") or "").strip()
    if not resolved_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your environment or .env file and try again."
        )

    resolved_model = (model or os.getenv("GROQ_MODEL") or "openai/gpt-oss-120b").strip()
    messages = build_messages(preferences)

    try:
        client = Groq(api_key=resolved_api_key)
        response = client.chat.completions.create(
            model=resolved_model,
            messages=messages,
            temperature=0.7,
            max_tokens=1400,
        )
        content = (response.choices[0].message.content or "").strip()
        if not content:
            raise RuntimeError("Groq returned an empty response.")
        return content
    except Exception as exc:  # noqa: BLE001 - convert API/runtime failures into friendly UI errors
        raise RuntimeError(f"Could not generate a workout plan: {exc}") from exc
