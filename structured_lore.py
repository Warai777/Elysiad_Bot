from archivist_lore import ARCHIVIST_LORE
from lore_tracker import LoreFragment

# Temporary mapping: phase-based fragment clustering (placeholder logic)
PHASE_TAGS = {
    "Intro": ["arrival", "origin", "entry"],
    "Exploration": ["memory", "map", "discovery"],
    "Climax": ["betrayal", "truth", "identity"],
    "Resolution": ["loss", "freedom", "archive"]
}

def get_structured_lore(world="Library of Beginnings", phase="Intro", tag=None):
    """
    Returns a list of LoreFragments that match world and phase.
    Optionally filter further by tag.
    """
    results = []
    for i, line in enumerate(ARCHIVIST_LORE):
        frag_tags = ["archivist"]
        if phase in PHASE_TAGS:
            frag_tags.extend(PHASE_TAGS[phase])
        if tag and tag not in frag_tags:
            continue
        frag = LoreFragment(
            fragment_id=f"archivist_{i}_p{phase}",
            title=f"[Phase: {phase}] Archivist Fragment {i+1}",
            text=line,
            tags=frag_tags,
            origin_world=world,
            discovery_method="phase_trigger"
        )
        results.append(frag)
    return results