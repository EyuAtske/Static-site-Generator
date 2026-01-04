import os
from pathlib import Path
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from markdown_tohtml import markdown_to_html_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    try:
        for block in blocks:
            if block_to_block_type(block) == BlockType.HEADING:
                txt = block.split(" ")
                if len(txt[0]) == 1:
                    title = " ".join(txt[1:]).strip()
                    return title
        raise ValueError
    except ValueError as v:
        print("There is no h1 element")
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, mode='r') as markdown_file:
        markdown = markdown_file.read()
        md = markdown_to_html_node(markdown).to_html()
    
    with open(template_path, mode='r') as temp_file:
        temp = temp_file.read()
        title = extract_title(markdown)
        template = temp.replace("{{ Title }}", f"{title}")
        template = template.replace("{{ Content }}", f"{md}")

    with open(dest_path, 'w') as f:
        f.write(template)
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(dir_path_content)
    if os.path.exists(dir_path_content):
        all_files = os.listdir(dir_path_content)
        file_to_page(dir_path_content, template_path, dest_dir_path, all_files)
    else:
        raise FileNotFoundError(f"{dir_path_content} does not exist")
def file_to_page(dir_path_content, template_path, dest_dir_path, files):
    for file in files:
        content_path = os.path.join(dir_path_content, file)
        if os.path.isfile(content_path):
            file_path = Path(content_path)
            if file_path.suffix.lower() == ".md":
                full_path = os.path.join(dest_dir_path, "index.html")
                generate_page(content_path, template_path, full_path)
        else:
            new_dest_dir = os.path.join(dest_dir_path, file)
            os.mkdir(new_dest_dir)
            new_dir = content_path
            next_files = os.listdir(new_dir)
            file_to_page(new_dir, template_path, new_dest_dir, next_files)