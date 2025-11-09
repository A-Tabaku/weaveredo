#!/usr/bin/env python3
"""
Complete Flow Test: Entry Agent → Character Development

This script tests the full pipeline:
1. Entry Agent (Intro_General_Entry) - Interactive Q&A
2. Character Development (Character_Identity) - 7 sub-agents with checkpoints
3. Final character profile output

Usage:
    python test_complete_flow.py [--auto-approve]

Options:
    --auto-approve    Automatically approve all checkpoints (for fast testing)
"""

import asyncio
import json
import time
import sys
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from agents.Intro_General_Entry.agent import EntryAgent
from agent_types import AgentLevel


# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """Print colorful header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.ENDC}\n")


def print_step(step_num, title):
    """Print step header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}STEP {step_num}: {title}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'-'*60}{Colors.ENDC}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}→ {text}{Colors.ENDC}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


async def run_entry_agent():
    """Run Entry Agent interactively to get character JSON"""
    print_step(1, "Entry Agent (Character Concept)")

    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print_error("ANTHROPIC_API_KEY not found in environment")
        sys.exit(1)

    # Initialize Entry Agent
    agent = EntryAgent(api_key=api_key, level=AgentLevel.Intro_General_Entry)
    conversation_history = []

    print_info("Entry Agent initialized. You can now describe your character concept.")
    print_info("The agent will ask you questions to build a complete character profile.")
    print_info("Type your responses naturally. The agent will output JSON when ready.")
    print()

    # Initial prompt to start the conversation
    print(f"{Colors.BOLD}Entry Agent:{Colors.ENDC} Hello! I'm here to help you develop a character. What kind of character would you like to create?")

    user_input = input(f"\n{Colors.BOLD}You:{Colors.ENDC} ").strip()

    while True:
        try:
            # Run agent
            response = await agent.run(user_input, conversation_history)

            # Check if response contains JSON (finalized output)
            if response.startswith("{") and "characters" in response:
                print_success("Entry Agent completed! Character JSON generated.")
                try:
                    character_json = json.loads(response)
                    return character_json
                except json.JSONDecodeError:
                    # Sometimes JSON is embedded in text
                    start = response.find("{")
                    end = response.rfind("}") + 1
                    character_json = json.loads(response[start:end])
                    return character_json

            # Print agent response
            print(f"\n{Colors.BOLD}Entry Agent:{Colors.ENDC} {response}")

            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": response})

            # Get next user input
            user_input = input(f"\n{Colors.BOLD}You:{Colors.ENDC} ").strip()

            if not user_input:
                print_warning("Empty input. Please provide a response.")
                user_input = input(f"\n{Colors.BOLD}You:{Colors.ENDC} ").strip()

        except Exception as e:
            print_error(f"Entry Agent error: {e}")
            raise


def start_character_development(entry_json):
    """Start character development via API"""
    print_step(2, "Character Development (7 Sub-Agents)")

    character_name = entry_json["characters"][0]["name"]
    print_info(f"Starting character development for '{character_name}'...")

    # Call API
    try:
        response = requests.post(
            "http://localhost:8000/api/character/start",
            json=entry_json,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        character_id = data["character_id"]
        print_success(f"Character ID: {character_id}")
        print_info(f"Status: {data['status']}")
        print_info(f"Total checkpoints: {data['checkpoint_count']}")

        return character_id

    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API server. Is it running?")
        print_info("Start server with: uvicorn api.server:app --port 8000")
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to start character development: {e}")
        raise


def monitor_progress(character_id, auto_approve=False):
    """Monitor character development progress and handle checkpoints"""
    print()
    print_info("Monitoring character development progress...")
    print_info("Agents are running in parallel waves...")
    print()

    completed_checkpoints = set()
    current_wave = 0

    wave_names = {
        1: "Wave 1: Foundation (Personality + Backstory)",
        2: "Wave 2: Expression (Voice + Physical + Story Arc)",
        3: "Wave 3: Social (Relationships + Images)"
    }

    while True:
        try:
            # Get status
            response = requests.get(f"http://localhost:8000/api/character/{character_id}/status")
            status_data = response.json()

            # Check if wave changed
            if status_data["current_wave"] != current_wave:
                current_wave = status_data["current_wave"]
                if current_wave <= 3:
                    print()
                    print(f"{Colors.YELLOW}{Colors.BOLD}{wave_names[current_wave]}{Colors.ENDC}")
                    print()

            # Check for new checkpoints
            for checkpoint_num in range(1, 9):
                if checkpoint_num in completed_checkpoints:
                    continue

                try:
                    checkpoint_response = requests.get(
                        f"http://localhost:8000/api/character/{character_id}/checkpoint/{checkpoint_num}"
                    )

                    if checkpoint_response.status_code == 200:
                        checkpoint_data = checkpoint_response.json()

                        if checkpoint_data["status"] == "awaiting_approval":
                            completed_checkpoints.add(checkpoint_num)
                            display_checkpoint(checkpoint_num, checkpoint_data, auto_approve)

                            if not auto_approve:
                                # Ask for approval
                                approve = input(f"\n{Colors.BOLD}Approve checkpoint #{checkpoint_num}? (y/n):{Colors.ENDC} ").strip().lower()

                                if approve == 'y':
                                    approve_checkpoint(character_id, checkpoint_num)
                                else:
                                    feedback = input(f"{Colors.BOLD}Provide feedback for regeneration:{Colors.ENDC} ").strip()
                                    if feedback:
                                        reject_checkpoint(character_id, checkpoint_num, feedback)
                            else:
                                # Auto-approve
                                approve_checkpoint(character_id, checkpoint_num)

                except:
                    pass

            # Check if all done
            if len(completed_checkpoints) >= 8:
                print_success("All checkpoints completed!")
                break

            # Wait before next poll
            time.sleep(2)

        except KeyboardInterrupt:
            print_warning("\nMonitoring interrupted by user")
            break
        except Exception as e:
            print_error(f"Monitoring error: {e}")
            time.sleep(2)


def display_checkpoint(checkpoint_num, data, auto_approve):
    """Display checkpoint information"""
    agent_name = data["agent"]
    output = data["output"]

    print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*60}")
    print(f"Checkpoint #{checkpoint_num}: {agent_name.replace('_', ' ').title()}")
    print(f"{'='*60}{Colors.ENDC}\n")

    # Show narrative
    print(f"{Colors.BOLD}Narrative:{Colors.ENDC}")
    narrative = output["narrative"]
    # Truncate if too long
    if len(narrative) > 500:
        print(narrative[:500] + "...")
        print(f"{Colors.CYAN}(Truncated. Full output in checkpoint file){Colors.ENDC}")
    else:
        print(narrative)

    print()

    # Show structured data summary
    print(f"{Colors.BOLD}Structured Data:{Colors.ENDC}")
    structured = output["structured"]

    if isinstance(structured, dict):
        for key, value in list(structured.items())[:5]:  # Show first 5 keys
            if isinstance(value, list):
                print(f"  • {key}: {len(value)} items")
            elif isinstance(value, str) and len(value) > 50:
                print(f"  • {key}: {value[:50]}...")
            else:
                print(f"  • {key}: {value}")

    if auto_approve:
        print()
        print_success(f"Auto-approved checkpoint #{checkpoint_num}")


def approve_checkpoint(character_id, checkpoint_num):
    """Approve a checkpoint"""
    try:
        requests.post(
            f"http://localhost:8000/api/character/{character_id}/approve",
            json={"checkpoint": checkpoint_num}
        )
        print_success(f"Checkpoint #{checkpoint_num} approved. Continuing...")
    except Exception as e:
        print_error(f"Failed to approve: {e}")


def reject_checkpoint(character_id, checkpoint_num, feedback):
    """Reject a checkpoint with feedback"""
    try:
        requests.post(
            f"http://localhost:8000/api/character/{character_id}/feedback",
            json={"checkpoint": checkpoint_num, "feedback": feedback}
        )
        print_info(f"Regenerating checkpoint #{checkpoint_num} with feedback...")
    except Exception as e:
        print_error(f"Failed to submit feedback: {e}")


def get_final_profile(character_id):
    """Get and display final character profile"""
    print_step(3, "Final Character Profile")

    try:
        response = requests.get(f"http://localhost:8000/api/character/{character_id}/final")

        if response.status_code == 404:
            print_warning("Final profile not yet ready. Waiting...")
            time.sleep(5)
            response = requests.get(f"http://localhost:8000/api/character/{character_id}/final")

        profile = response.json()

        print_success("Character development complete!")
        print()
        print(f"{Colors.BOLD}Character: {profile['name']}{Colors.ENDC}")
        print(f"Role: {profile['overview']['role']}")
        print(f"Completed: {profile['completed_at']}")
        print()

        # Save to file
        filename = f"character_{profile['name'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(profile, f, indent=2)

        print_success(f"Profile saved to: {filename}")
        print()

        # Show some highlights
        print(f"{Colors.BOLD}Character Highlights:{Colors.ENDC}")

        if 'psychology' in profile:
            print(f"\n  Traits: {', '.join(profile['psychology']['core_traits'][:3])}")
            print(f"  Fears: {', '.join(profile['psychology']['fears'][:2])}")

        if 'voice' in profile and 'sample_dialogue' in profile['voice']:
            dialogue = profile['voice']['sample_dialogue']
            if 'confident' in dialogue:
                print(f"\n  Sample Dialogue: \"{dialogue['confident']}\"")

        if 'visual' in profile and 'images' in profile['visual']:
            print(f"\n  Generated Images: {len(profile['visual']['images'])}")
            for img in profile['visual']['images']:
                print(f"    • {img['type']}: {img['url']}")

        print()
        print_info(f"Full character data: backend/character_data/{character_id}/")

    except Exception as e:
        print_error(f"Failed to get final profile: {e}")


async def main():
    """Run complete flow test"""
    # Parse args
    auto_approve = "--auto-approve" in sys.argv

    print_header("WEAVE AGENT SYSTEM - COMPLETE FLOW TEST")
    print(f"{Colors.BOLD}Testing: Entry Agent → Character Development → Final Profile{Colors.ENDC}")

    if auto_approve:
        print_warning("Auto-approve mode enabled. All checkpoints will be automatically approved.")

    try:
        # Step 1: Run Entry Agent
        entry_json = await run_entry_agent()

        print()
        print_success("Entry Agent output:")
        print(json.dumps(entry_json, indent=2)[:500] + "...")
        print()

        input(f"{Colors.BOLD}Press Enter to continue to Character Development...{Colors.ENDC}")

        # Step 2: Start Character Development
        character_id = start_character_development(entry_json)

        print()
        input(f"{Colors.BOLD}Press Enter to start monitoring progress...{Colors.ENDC}")

        # Step 3: Monitor progress and checkpoints
        monitor_progress(character_id, auto_approve)

        # Step 4: Get final profile
        get_final_profile(character_id)

        print_header("TEST COMPLETE!")
        print_success("Full pipeline tested successfully!")

    except KeyboardInterrupt:
        print()
        print_warning("Test interrupted by user")
    except Exception as e:
        print_error(f"Test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
