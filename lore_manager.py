from archivist_lore import ARCHIVIST_LORE

def unlock_lore(player, index):
    if index < 0 or index >= len(ARCHIVIST_LORE):
        return False
    if ARCHIVIST_LORE[index] not in player.memory["Journal"]["Lore"]:
        player.memory["Journal"]["Lore"].append(ARCHIVIST_LORE[index])
        return True
    return False

def has_lore(player, index):
    if index < 0 or index >= len(ARCHIVIST_LORE):
        return False
    return ARCHIVIST_LORE[index] in player.memory["Journal"]["Lore"]

def get_lore_pages(player, page_index=0, entries_per_page=2):
    lore_entries = player.memory["Journal"].get("Lore", [])
    total_pages = max(1, (len(lore_entries) + entries_per_page - 1) // entries_per_page)
    page_index = max(0, min(page_index, total_pages - 1))

    start = page_index * entries_per_page
    end = start + entries_per_page
    page_content = lore_entries[start:end]

    # Ensure 2 items for left and right page formatting
    if len(page_content) == 1:
        page_content.append("")
    elif len(page_content) == 0:
        page_content = ["", ""]

    return {
        "left": page_content[0],
        "right": page_content[1],
        "current_page": page_index,
        "total_pages": total_pages
    }