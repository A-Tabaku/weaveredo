"""
Backstory & Motivation Sub-Agent (Wave 1)

Develops character's history and goals including:
- Detailed timeline of life events
- Formative experiences
- Surface goals vs deep psychological needs
- Internal conflicts between competing desires
"""

import json
from typing import Tuple
from anthropic import Anthropic

from ..schemas import CharacterKnowledgeBase, BackstoryOutput, TimelineEvent


async def backstory_motivation_agent(
    kb: CharacterKnowledgeBase,
    api_key: str
) -> Tuple[BackstoryOutput, str]:
    """
    Generate detailed backstory and motivation profile

    Args:
        kb: Character knowledge base with input data
        api_key: Anthropic API key

    Returns:
        Tuple of (BackstoryOutput, narrative_description)
    """
    client = Anthropic(api_key=api_key)
    model = "claude-sonnet-4-5-20250929"

    # Extract data
    character = kb["input_data"]["characters"][0]
    storyline = kb["input_data"]["storyline"]
    mode = kb.get("mode", "balanced")

    # Use personality data if available (Wave 1 agents run in parallel, might not be available)
    personality_context = ""
    if kb.get("personality"):
        personality_context = f"""
PERSONALITY INSIGHTS (from Personality Agent):
- Core Traits: {", ".join(kb["personality"]["core_traits"])}
- Fears: {", ".join(kb["personality"]["fears"])}
- Secrets: {", ".join(kb["personality"]["secrets"])}

Use these insights to inform backstory development."""

    system_prompt = f"""You are a character development expert specializing in backstory and motivation for {storyline["tone"]} stories.

Your task is to create a detailed backstory and motivation profile for this character.

CHARACTER OVERVIEW:
- Name: {character["name"]}
- Basic Info: {character["personality"]}
- Appearance: {character["appearance"]}
- Role: {character["role"]}
- Story Context: {storyline["overview"]}
{personality_context}

DEPTH MODE: {mode}
{"Create essential timeline and motivations only." if mode == "fast" else ""}
{"Provide comprehensive backstory with rich detail and complexity." if mode == "deep" else ""}
{"Balance depth with narrative efficiency." if mode == "balanced" else ""}

OUTPUT REQUIREMENTS:

1. TIMELINE (5-10 key events)
   - Start from childhood or significant early event
   - Progress to present day
   - Include ages and major life events
   - Each event should shape who they became
   - Format: [{{"age": X, "event": "description"}}, ...]

2. FORMATIVE EXPERIENCES (3-5 experiences)
   - Deep dive into 3-5 crucial moments that shaped them
   - Explain HOW each experience influenced their personality
   - Connect to their current behavior and beliefs

3. GOALS
   - Surface goals: What they SAY they want or consciously pursue
   - Deep goals: What they ACTUALLY need (often unconscious)
   - These should conflict or be different
   - Format: {{"surface": "...", "deep": "..."}}

4. INTERNAL CONFLICTS (2-4 conflicts)
   - Competing desires that create tension
   - Example: "Wanting connection vs. fear of vulnerability"
   - Should drive character behavior and decisions

IMPORTANT:
- Make backstory SPECIFIC and unique to this character
- Ensure timeline events logically lead to who they are now
- Connect backstory to personality traits
- Create rich motivation beyond simple "good guy wants to save world"

First, provide a rich NARRATIVE backstory (3-4 paragraphs covering their past, formative moments, and what drives them).
Then, provide the STRUCTURED data in JSON format.

Format:
NARRATIVE:
[Your narrative here]

STRUCTURED:
{{
  "timeline": [
    {{"age": 12, "event": "..."}},
    {{"age": 18, "event": "..."}},
    ...
  ],
  "formative_experiences": [
    "Experience 1 and its impact...",
    "Experience 2 and its impact...",
    ...
  ],
  "goals": {{
    "surface": "What they consciously pursue",
    "deep": "What they truly need"
  }},
  "internal_conflicts": [
    "Conflict 1",
    "Conflict 2",
    ...
  ]
}}"""

    # Make API call
    response = client.messages.create(
        model=model,
        max_tokens=5000,
        temperature=0.7,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Create a detailed backstory and motivation profile for {character['name']}. Provide both narrative and structured output."
        }]
    )

    # Parse response
    content = response.content[0].text

    # Split narrative and structured
    parts = content.split("STRUCTURED:")
    if len(parts) == 2:
        narrative = parts[0].replace("NARRATIVE:", "").strip()
        structured_text = parts[1].strip()
    else:
        narrative = content[:content.find("{")].strip() if "{" in content else content
        structured_text = content[content.find("{"):content.rfind("}")+1] if "{" in content else "{}"

    # Parse JSON
    try:
        if "```json" in structured_text:
            structured_text = structured_text.split("```json")[1].split("```")[0]
        elif "```" in structured_text:
            structured_text = structured_text.split("```")[1].split("```")[0]

        structured_data = json.loads(structured_text)
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse backstory JSON: {e}")
        structured_data = {
            "timeline": [{"age": 20, "event": "Significant event"}],
            "formative_experiences": ["Key experience"],
            "goals": {"surface": "Unknown", "deep": "Unknown"},
            "internal_conflicts": ["Internal struggle"]
        }

    # Create output
    backstory_output: BackstoryOutput = {
        "timeline": structured_data.get("timeline", []),
        "formative_experiences": structured_data.get("formative_experiences", []),
        "goals": structured_data.get("goals", {}),
        "internal_conflicts": structured_data.get("internal_conflicts", [])
    }

    return backstory_output, narrative
