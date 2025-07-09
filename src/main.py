from textnode import *
from textnode import TextType,TextNode
from block_markdown import markdown_to_html_node
from static_to_public import static_to_public
from pathlib import Path
import sys
import os

def main():
    basepath = "/"
    if len(sys.argv)>1:
        basepath=sys.argv[1]

    static_to_public()
    print("Current working directory:", os.getcwd())
    print("Looking for content at:", os.path.abspath("content/index.md"))
    print("Looking for template at:", os.path.abspath("template.html"))
    generate_pages_recursive("content/","template.html","docs/",basepath)

def generate_pages_recursive(dir_path_content,template_path,dest_dir_path,basepath):
    paths = os.listdir(dir_path_content)
    for path in paths:
        curr_path = os.path.join(dir_path_content,path)
        dest_path = os.path.join(dest_dir_path,path)
        if os.path.isfile(curr_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(curr_path,template_path,dest_path,basepath)
        else:
            generate_pages_recursive(curr_path,template_path,dest_path,basepath)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line[2:]
    raise Exception("No Header found")

def generate_page(from_path,template_path,dest_path,basepath):
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
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)
    




if __name__ == "__main__":
    main()