from textnode import *
from textnode import TextType,TextNode
from block_markdown import markdown_to_html_node
from static_to_public import static_to_public
import os
def main():
    static_to_public()
    print("Current working directory:", os.getcwd())
    print("Looking for content at:", os.path.abspath("content/index.md"))
    print("Looking for template at:", os.path.abspath("template.html"))
    generate_page("content/index.md","template.html","public/index.html")
    

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line[2:]
    raise Exception("No Header found")

def generate_page(from_path,template_path,dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if os.path.isfile(from_path):
        with open(from_path, 'r') as f:
            content = f.read()
    if os.path.isfile(template_path):
        with open(template_path, 'r') as f:
            template = f.read()
    x = markdown_to_html_node(content)
    html_string = x.to_html()
    title = extract_title(content)
    template =template.replace("{{ Title }}",title)
    template =template.replace("{{ Content }}",html_string)
    if len(os.path.dirname(dest_path)) != 0:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path,'w') as f:
        f.write(template)
    




if __name__ == "__main__":
    main()