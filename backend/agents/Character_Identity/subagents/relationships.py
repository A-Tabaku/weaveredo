"""
Relationships Sub-Agent (Wave 3)

Develops character's interpersonal connections including:
- Character-to-character relationship mapping
- Connection types (allies, enemies, family, romantic, rivals, mentors)
- Power dynamics and relationship evolution
- How they behave differently with different people
"""

import json
from typing import Tuple, List
from anthropic import Anthropic

from ..schemas import CharacterKnowledgeBase, RelationshipsOutput, Relationship


async def relationships_agent(
    kb: CharacterKnowledgeBase,
    api_key: str
) -> Tuple[RelationshipsOutput, str]:
    """
    Generate detailed relationship dynamics profile

    Args:
        kb: Character knowledge base (requires Wave 1+2 outputs)
        api_key: Anthropic API key

    Returns:
        Tuple of (RelationshipsOutput, narrative_description)
    """
    client = Anthropic(api_key=api_key)
    model = "claude-sonnet-4-5-20250929"

    # Extract data
    character = kb["input_data"]["characters"][0]
    storyline = kb["input_data"]["storyline"]
    mode = kb.get("mode", "balanced")

    # Build comprehensive context from all previous outputs
    context_blocks = []

    if kb.get("personality"):
        p = kb["personality"]
        context_blocks.append(f"""PERSONALITY:
- Traits: {", ".join(p["core_traits"])}
- Fears: {", ".join(p["fears"])} (affects trust and relationships)
- Triggers: {", ".join(p["triggers"])}""")

    if kb.get("backstory_motivation"):
        b = kb["backstory_motivation"]
        context_blocks.append(f"""BACKSTORY:
- Key Events: {", ".join([e.get("event", "")[:60] for e in b["timeline"][:3]])}
- Internal Conflicts: {", ".join(b["internal_conflicts"])}
(Past shapes relationship patterns)""")

    if kb.get("story_arc"):
        sa = kb["story_arc"]
        context_blocks.append(f"""STORY ARC:
- Role: {sa["role"]}
- Arc Type: {sa["arc_type"]}
(Relationships should support this narrative arc)""")

    full_context = "\n\n".join(context_blocks)

    system_prompt = f"""You are a relationship dynamics expert creating a character's interpersonal connections for a {storyline["tone"]} story.

Your task is to define this character's KEY RELATIONSHIPS and how they interact with others.

CHARACTER OVERVIEW:
- Name: {character["name"]}
- Role: {character["role"]}
- Story Context: {storyline["overview"]}

{full_context}

DEPTH MODE: {mode}

OUTPUT REQUIREMENTS:

Create 3-6 significant relationships for this character. For EACH relationship, define:

1. CHARACTER (who they're connected to)
   - Can be named if from the story, or "TBD - [role]" if not yet defined
   - Examples: "The Mentor (TBD)", "Sarah Martinez", "The Crime Boss (antagonist, TBD)"

2. TYPE (relationship category)
   - Examples: mentor_figure, antagonist, ally, family (specify: mother, sibling, etc.), romantic_interest, rival, friend, enemy, authority_figure, foil, etc.
   - Be specific

3. DYNAMIC (how they interact)
   - Power dynamics: Who has power? Equal? Shifting?
   - Emotional tone: Trust? Tension? Love? Fear? Respect?
   - What this relationship reveals about the character
   - Key conflicts or harmony

4. EVOLUTION (how relationship changes)
   - Start of story → End of story progression
   - Moments that shift the relationship
   - Do they grow closer, further apart, or transform?

IMPORTANT GUIDELINES:
- Relationships should reflect personality (e.g., trust issues → few close bonds)
- Connect to backstory (e.g., family estrangement from past events)
- Support story arc (redemption arc → strained relationships that heal)
- Include diverse relationship types (not all allies or all enemies)
- Make dynamics SPECIFIC and complex (not just "friends" or "enemies")

NOTE: Since other characters may not be fully developed yet, you can use placeholder descriptions like:
- "The Mentor (TBD - unnamed)" if their mentor hasn't been created
- But still define the DYNAMIC and EVOLUTION based on this character's needs

First, provide a rich NARRATIVE description of their relationship patterns and key connections (2-3 paragraphs).
Then, provide the STRUCTURED data in JSON format.

Format:
NARRATIVE:
[Your narrative here]

STRUCTURED:
{{
  "relationships": [
    {{
      "character": "Name or TBD with description",
      "type": "relationship_type",
      "dynamic": "Detailed description of interaction...",
      "evolution": "How relationship changes..."
    }},
    ...
  ]
}}"""

    # Make API call
    response = client.messages.create(
        model=model,
        max_tokens=4500,
        temperature=0.7,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Create a detailed relationships profile for {character['name']}. Provide both narrative and structured output."
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
        print(f"Warning: Failed to parse relationships JSON: {e}")
        structured_data = {
            "relationships": [
                {
                    "character": "Unknown",
                    "type": "unknown",
                    "dynamic": "Unknown",
                    "evolution": "Unknown"
                }
            ]
        }

    # Create output
    relationships_output: RelationshipsOutput = {
        "relationships": structured_data.get("relationships", [])
    }

    return relationships_output, narrative
