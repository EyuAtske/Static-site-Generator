from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    new_lines = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        l = []
        for part in line.split("\n"):
            l.append(part.strip())
        new_lines.append("\n".join(l))
    return new_lines
def block_to_block_type(mk_text):
    text = mk_text.split("\n")
    inorder = 1
    if mk_text.startswith("#"):
        return BlockType.HEADING
    elif mk_text.startswith("```") and mk_text.endswith("```"):
        return BlockType.CODE
    elif mk_text.startswith(">"):
        return BlockType.QUOTE
    elif mk_text.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif mk_text.startswith("1. "):
        if len(text) == 1:
            return BlockType.ORDERED_LIST
        for line in text:
            if line.startswith(f"{inorder}. "):
                inorder += 1
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH