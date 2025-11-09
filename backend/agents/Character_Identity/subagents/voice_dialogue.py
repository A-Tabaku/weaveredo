"""
Voice & Dialogue Sub-Agent (Wave 2)

Develops character's speech patterns and communication style including:
- Speech patterns (formal, casual, fragmented, etc.)
- Verbal tics and characteristic phrases
- Vocabulary level and word choices
- Sample dialogue in different emotional states
"""

import json
from typing import Tuple
from anthropic import AsyncAnthropic  # FIX: Use AsyncAnthropic for async functions

from ..schemas import CharacterKnowledgeBase, VoiceOutput, SampleDialogue


async def voice_dialogue_agent(
    kb: CharacterKnowledgeBase,
    api_key: str
) -> Tuple[VoiceOutput, str]:
    """
    Generate detailed voice and dialogue profile

    Args:
        kb: Character knowledge base (requires Wave 1 outputs)
        api_key: Anthropic API key

    Returns:
        Tuple of (VoiceOutput, narrative_description)
    """
    client = AsyncAnthropic(api_key=api_key)  # FIX: Use AsyncAnthropic
    model = "claude-haiku-4-5-20251001"

    # Extract data
    character = kb["input_data"]["characters"][0]
    storyline = kb["input_data"]["storyline"]
    mode = kb.get("mode", "balanced")

    # Build context from Wave 1 outputs
    personality_context = ""
    if kb.get("personality"):
        p = kb["personality"]
        personality_context = f"""
PERSONALITY:
- Traits: {", ".join(p["core_traits"])}
- Emotional Baseline: {p["emotional_baseline"]}
- Fears: {", ".join(p["fears"])}"""

    backstory_context = ""
    if kb.get("backstory_motivation"):
        b = kb["backstory_motivation"]
        backstory_context = f"""
BACKSTORY:
- Background influences their speech patterns
- Goals: {b["goals"].get("surface", "Unknown")} (surface), {b["goals"].get("deep", "Unknown")} (deep)"""

    system_prompt = f"""You are a dialogue and voice expert creating a character's unique speech patterns for a {storyline["tone"]} story.

Your task is to define HOW this character speaks, including their vocabulary, patterns, and voice.

CHARACTER OVERVIEW:
- Name: {character["name"]}
- Role: {character["role"]}
- Story Tone: {storyline["tone"]}
{personality_context}
{backstory_context}

DEPTH MODE: {mode}

OUTPUT REQUIREMENTS:

1. SPEECH PATTERN (detailed description)
   - Overall style: formal, casual, fragmented, poetic, terse, rambling?
   - Sentence structure: Complete sentences, fragments, run-ons?
   - Rhythm and pacing: Fast talker, deliberate, pauses?
   - Regional dialect or accent influences?
   - How do they sound different in different contexts?

2. VERBAL TICS (3-6 specific tics)
   - Repeated words/phrases they use constantly
   - Filler words: "like", "um", "you know", "look", "listen"
   - Characteristic expressions unique to them
   - Nervous habits in speech

3. VOCABULARY (description)
   - Education level reflected in word choice
   - Working-class vs academic vs street slang
   - Technical jargon or specialized language?
   - Old-fashioned or modern expressions

4. SAMPLE DIALOGUE
   - Confident state: How they talk when self-assured
   - Vulnerable state: How they talk when hurt/scared
   - Stressed state: How they talk under pressure
   - Sarcastic state: How they use humor/deflection

   Each sample should be 1-2 sentences that SOUNDS like them

IMPORTANT:
- Make voice DISTINCT and recognizable
- Connect speech to personality (e.g., cynical → sarcastic tone)
- Consider backstory impact (e.g., street kid → slang)
- Sample dialogue should SHOW their voice, not just describe it

First, provide a rich NARRATIVE description of their voice (2-3 paragraphs explaining how they sound and why).
Then, provide the STRUCTURED data in JSON format.

Format:
NARRATIVE:
[Your narrative here]

STRUCTURED:
{{
  "speech_pattern": "Detailed description...",
  "verbal_tics": ["tic1", "tic2", ...],
  "vocabulary": "Description of word choices...",
  "sample_dialogue": {{
    "confident": "Example line...",
    "vulnerable": "Example line...",
    "stressed": "Example line...",
    "sarcastic": "Example line..."
  }}
}}"""

    # Make API call (FIX: Add await for async client)
    response = await client.messages.create(
        model=model,
        max_tokens=4000,
        temperature=0.8,  # Higher temp for creative dialogue
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Create a detailed voice and dialogue profile for {character['name']}. Provide both narrative and structured output."
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
        print(f"Warning: Failed to parse voice JSON: {e}")
        structured_data = {
            "speech_pattern": "Unknown",
            "verbal_tics": ["..."],
            "vocabulary": "Unknown",
            "sample_dialogue": {
                "confident": "...",
                "vulnerable": "...",
                "stressed": "...",
                "sarcastic": "..."
            }
        }

    # Create output
    voice_output: VoiceOutput = {
        "speech_pattern": structured_data.get("speech_pattern", ""),
        "verbal_tics": structured_data.get("verbal_tics", []),
        "vocabulary": structured_data.get("vocabulary", ""),
        "sample_dialogue": structured_data.get("sample_dialogue", {})  # type: ignore
    }

    return voice_output, narrative
