"""
Physical Description Sub-Agent (Wave 2)

Develops character's embodied movement and physicality including:
- Physical mannerisms and habitual tics
- Body language and posture
- Physical quirks and nervous habits
- Movement patterns and how they inhabit space
"""

import json
from typing import Tuple
from anthropic import Anthropic

from ..schemas import CharacterKnowledgeBase, PhysicalOutput


async def physical_description_agent(
    kb: CharacterKnowledgeBase,
    api_key: str
) -> Tuple[PhysicalOutput, str]:
    """
    Generate detailed physical presence and movement profile

    Args:
        kb: Character knowledge base (requires Wave 1 outputs)
        api_key: Anthropic API key

    Returns:
        Tuple of (PhysicalOutput, narrative_description)
    """
    client = Anthropic(api_key=api_key)
    model = "claude-sonnet-4-5-20250929"

    # Extract data
    character = kb["input_data"]["characters"][0]
    storyline = kb["input_data"]["storyline"]
    mode = kb.get("mode", "balanced")

    # Build context from previous outputs
    personality_context = ""
    if kb.get("personality"):
        p = kb["personality"]
        personality_context = f"""
PERSONALITY:
- Traits: {", ".join(p["core_traits"])}
- Fears: {", ".join(p["fears"])}
- Triggers: {", ".join(p["triggers"])}
(These should influence body language and physical habits)"""

    backstory_context = ""
    if kb.get("backstory_motivation"):
        b = kb["backstory_motivation"]
        timeline_summary = ", ".join([f"{e.get('age', 'Unknown')}: {e.get('event', '')[:50]}" for e in b["timeline"][:3]])
        backstory_context = f"""
KEY BACKSTORY EVENTS:
{timeline_summary}
(Past experiences shape physical habits and posture)"""

    system_prompt = f"""You are a physical movement and body language expert creating a character's unique physical presence for a {storyline["tone"]} story.

Your task is to define HOW this character MOVES, their physical habits, and how they inhabit space.

CHARACTER OVERVIEW:
- Name: {character["name"]}
- Basic Appearance: {character["appearance"]}
- Role: {character["role"]}
{personality_context}
{backstory_context}

DEPTH MODE: {mode}

OUTPUT REQUIREMENTS:

1. MANNERISMS (4-6 specific mannerisms)
   - Habitual physical tics they do constantly
   - NOT generic ("scratches head") - make it SPECIFIC and character-defining
   - Examples: "always scans exits when entering a room", "fidgets with wedding ring even after divorce"
   - Connect to personality/backstory

2. BODY LANGUAGE (detailed description)
   - Default posture: Hunched? Straight? Relaxed? Tense?
   - How they stand, sit, occupy space
   - Open or closed body language?
   - Confident or cautious physical presence?
   - How posture changes in different emotional states

3. MOVEMENT STYLE (description)
   - How they walk: Stride, shuffle, slink, march?
   - Speed and rhythm of movement
   - Graceful or clumsy? Loud or quiet?
   - How they gesture when talking
   - Physical energy level (restless, languid, measured)

4. PHYSICAL QUIRKS (3-5 specific quirks)
   - Unique physical habits tied to personality
   - Examples: "cracks knuckles before confrontation", "tilts head when suspicious", "taps foot when impatient"
   - Nervous habits vs. confident habits
   - What they do with their hands when stressed/relaxed

IMPORTANT:
- Make physical traits SPECIFIC and unique
- Connect movement to psychology (e.g., fear of betrayal → always watches exits)
- Consider backstory impact (e.g., former soldier → military posture)
- Avoid clichés - make it distinctive

First, provide a rich NARRATIVE description of their physical presence (2-3 paragraphs explaining how they move and why).
Then, provide the STRUCTURED data in JSON format.

Format:
NARRATIVE:
[Your narrative here]

STRUCTURED:
{{
  "mannerisms": [
    "Specific mannerism 1",
    "Specific mannerism 2",
    ...
  ],
  "body_language": "Detailed description of posture and presence...",
  "movement_style": "Description of how they move through space...",
  "physical_quirks": [
    "Quirk 1",
    "Quirk 2",
    ...
  ]
}}"""

    # Make API call
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        temperature=0.7,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Create a detailed physical presence profile for {character['name']}. Provide both narrative and structured output."
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
        print(f"Warning: Failed to parse physical JSON: {e}")
        structured_data = {
            "mannerisms": ["Unknown mannerism"],
            "body_language": "Unknown",
            "movement_style": "Unknown",
            "physical_quirks": ["Unknown quirk"]
        }

    # Create output
    physical_output: PhysicalOutput = {
        "mannerisms": structured_data.get("mannerisms", []),
        "body_language": structured_data.get("body_language", ""),
        "movement_style": structured_data.get("movement_style", ""),
        "physical_quirks": structured_data.get("physical_quirks", [])
    }

    return physical_output, narrative
