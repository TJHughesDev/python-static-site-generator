import os
from markdown_blocks import extract_title, markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} using {template_path} to {dest_path}")
    
    if not os.path.isfile(from_path):
        raise FileNotFoundError(f"Source file does not exist: {from_path}")

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    # is this valid python synatx?
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    final_html = (
        html_template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_string)
    )
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Page successfully generated: {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Loop through all items in the content directory
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        # If entry is a directory → recurse
        if os.path.isdir(entry_path):
            # ensure dest directory exists
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            generate_pages_recursive(entry_path, template_path, dest_path)

        # If entry is a markdown file → generate a page
        elif os.path.isfile(entry_path) and entry.endswith(".md"):
            html_filename = entry.replace(".md", ".html")
            dest_file = os.path.join(dest_dir_path, html_filename)

            generate_page(
                from_path=entry_path,
                template_path=template_path,
                dest_path=dest_file
            )



    