"""
Personality Sub-Agent (Wave 1)

Analyzes and expands character's core psychological makeup including:
- Core personality traits
- Fears and triggers
- Secrets (psychological dimension)
- Emotional patterns and baselines
"""

import os
from typing import Dict, Tuple
from anthropic import AsyncAnthropic  # FIX: Use AsyncAnthropic for async functions

from ..schemas import CharacterKnowledgeBase, PersonalityOutput


async def personality_agent(
    kb: CharacterKnowledgeBase,
    api_key: str
) -> Tuple[PersonalityOutput, str]:
    """
    Generate detailed personality profile

    Args:
        kb: Character knowledge base with input data
        api_key: Anthropic API key

    Returns:
        Tuple of (PersonalityOutput, narrative_description)
    """
    client = AsyncAnthropic(api_key=api_key)  # FIX: Use AsyncAnthropic
    model = "claude-haiku-4-5-20251001"  # Using Haiku for speed + cost efficiency

    # Extract character info from input
    character = kb["input_data"]["characters"][0]
    storyline = kb["input_data"]["storyline"]
    mode = kb.get("mode", "balanced")

    # Build system prompt
    system_prompt = f"""You are a character psychology expert analyzing a character for a {storyline["tone"]} story.

Your task is to expand the character's personality into a comprehensive psychological profile.

CHARACTER OVERVIEW:
- Name: {character["name"]}
- Basic Personality: {character["personality"]}
- Appearance: {character["appearance"]}
- Role: {character["role"]}
- Story Context: {storyline["overview"]}
- Tone: {storyline["tone"]}

DEPTH MODE: {mode}
{"Focus on essential psychological elements only." if mode == "fast" else ""}
{"Provide comprehensive analysis with depth and nuance." if mode == "deep" else ""}
{"Balance depth with efficiency." if mode == "balanced" else ""}

OUTPUT REQUIREMENTS:
Generate a detailed personality analysis including:

1. CORE TRAITS (4-6 traits)
   - Fundamental personality characteristics
   - Internal contradictions and complexities
   - How traits interact and conflict

2. FEARS (2-4 deep fears)
   - Not surface-level phobias, but psychological fears
   - What terrifies them emotionally/existentially
   - Trauma responses and triggers

3. SECRETS (2-3 significant secrets)
   - What they hide from others
   - What they hide from themselves (psychological dimension)
   - Shame, guilt, hidden desires

4. EMOTIONAL BASELINE
   - Their "default" emotional state
   - How they present vs how they feel
   - Emotional range and volatility

5. TRIGGERS (3-5 specific triggers)
   - What situations/words/people trigger strong reactions
   - Both positive and negative triggers
   - Why these things affect them

IMPORTANT:
- Make it SPECIFIC to this character, not generic
- Consider their backstory ({character.get("personality", "")})
- Ensure psychological depth and complexity
- Make traits interconnected and coherent

First, provide a rich NARRATIVE description of their psychology (2-3 paragraphs).
Then, provide the STRUCTURED data in JSON format.

Format:
NARRATIVE:
[Your narrative here]

STRUCTURED:
{{
  "core_traits": ["trait1", "trait2", ...],
  "fears": ["fear1", "fear2", ...],
  "secrets": ["secret1", "secret2", ...],
  "emotional_baseline": "description",
  "triggers": ["trigger1", "trigger2", ...]
}}"""

    # Make API call (FIX: Add await for async client)
    response = await client.messages.create(
        model=model,
        max_tokens=4000,
        temperature=0.7,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Analyze {character['name']}'s personality in depth. Provide both narrative and structured output."
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
        # Fallback if format not followed
        narrative = content[:content.find("{")].strip() if "{" in content else content
        structured_text = content[content.find("{"):content.rfind("}")+1] if "{" in content else "{}"

    # Parse JSON
    import json
    try:
        # Extract JSON from markdown code blocks if present
        if "```json" in structured_text:
            structured_text = structured_text.split("```json")[1].split("```")[0]
        elif "```" in structured_text:
            structured_text = structured_text.split("```")[1].split("```")[0]

        structured_data = json.loads(structured_text)
    except json.JSONDecodeError as e:
        # Fallback to basic structure
        print(f"Warning: Failed to parse personality JSON: {e}")
        structured_data = {
            "core_traits": ["complex", "conflicted"],
            "fears": ["unknown"],
            "secrets": ["hidden past"],
            "emotional_baseline": "guarded",
            "triggers": ["personal questions"]
        }

    # Validate and create output
    personality_output: PersonalityOutput = {
        "core_traits": structured_data.get("core_traits", []),
        "fears": structured_data.get("fears", []),
        "secrets": structured_data.get("secrets", []),
        "emotional_baseline": structured_data.get("emotional_baseline", ""),
        "triggers": structured_data.get("triggers", [])
    }

    return personality_output, narrative
