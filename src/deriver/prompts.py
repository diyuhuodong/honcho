"""
Minimal prompts for the deriver module optimized for speed.

This module contains simplified prompt templates focused only on observation extraction.
NO peer card instructions, NO working representation - just extract observations.
"""

from functools import cache
from inspect import cleandoc as c

from src.utils.tokens import estimate_tokens


def minimal_deriver_prompt(
    peer_id: str,
    messages: str,
) -> str:
    """
    Generate minimal prompt for fast observation extraction.

    Args:
        peer_id: The ID of the user being analyzed.
        messages: All messages in the range (interleaving messages and new turns combined).

    Returns:
        Formatted prompt string for observation extraction.
    """
    return c(
        f"""
Analyze messages from {peer_id} to extract **explicit atomic facts** about them.

[EXPLICIT] DEFINITION: Facts about {peer_id} that can be derived directly from their messages.
   - Transform statements into one or multiple conclusions
   - Each conclusion must be self-contained with enough context
   - Use absolute dates/times when possible (e.g. "June 26, 2025" not "yesterday")

RULES:
- Properly attribute observations to the correct subject: if it is about {peer_id}, say so. If {peer_id} is referencing someone or something else, make that clear.
- Observations should make sense on their own. Each observation will be used in the future to better understand {peer_id}.
- Extract ALL observations from {peer_id} messages, using others as context.
- Contextualize each observation sufficiently (e.g. "Ann is nervous about the job interview at the pharmacy" not just "Ann is nervous")
- Return your response as JSON with an "explicit" array containing objects with "content" field only. No other fields or text.

Messages to analyze:
<messages>
{messages}
</messages>

Respond with JSON only:
"""
    )


@cache
def estimate_minimal_deriver_prompt_tokens() -> int:
    """Estimate base prompt tokens (cached)."""
    try:
        prompt = minimal_deriver_prompt(
            peer_id="",
            messages="",
        )
        return estimate_tokens(prompt)
    except Exception:
        return 300
