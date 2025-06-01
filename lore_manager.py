from lore_tracker import LoreFragment
from archivist_lore import ARCHIVIST_LORE

# Convert string lore into structured LoreFragment objects
def get_all_archivist_lore():
    fragments = []
    for i, line in enumerate(ARCHIVIST_LORE):
        frag = LoreFragment(
            fragment_id=f"archivist_{i}",
            title=f"Archivist Fragment {i+1}",
            text=line,
            tags=["archivist", "memory"],
            origin_world="Library of Beginnings",
            discovery_method="system_default"
        )
        fragments.append(frag)
    return fragments

def unlock_lore(tracker, frag: LoreFragment):
    if not tracker.is_unlocked(frag.id):
        tracker.unlock(frag)
        return True
    return False

def has_lore(tracker, fragment_id):
    return tracker.is_unlocked(fragment_id)

def get_lore_pages(tracker, page_index=0, entries_per_page=2):
    lore_entries = tracker.get_all_unlocked()
    total_pages = max(1, (len(lore_entries) + entries_per_page - 1) // entries_per_page)
    page_index = max(0, min(page_index, total_pages - 1))

    start = page_index * entries_per_page
    end = start + entries_per_page
    page_content = lore_entries[start:end]

    if len(page_content) == 1:
        page_content.append(None)
    elif len(page_content) == 0:
        page_content = [None, None]

    return {
        "left": page_content[0],
        "right": page_content[1],
        "current_page": page_index,
        "total_pages": total_pages
    }

def get_lore_by_tag(tracker, tag):
    return [frag for frag in tracker.get_all_unlocked() if tag in frag.tags]

def get_lore_by_world(tracker, world):
    return [frag for frag in tracker.get_all_unlocked() if frag.origin_world == world]