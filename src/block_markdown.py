from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode,ParentNode
from textnode import TextNode, TextType,text_node_to_html_node
from inline_markdown import text_to_textnodes
class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h1"
    QUOTE = "blockquote"
    CODE = "code"
    ULIST = "ul"
    OLIST = "ol"

def block_to_block_type(markdown):
    if re.match(r'^(#{1,6})\s+(.*)$',markdown):
        return BlockType.HEADING
    elif markdown.endswith("```") and markdown.startswith("```"):
        return BlockType.CODE
    lines = markdown.split("\n")
    quote = True
    unordered_list = True
    ordered_list = True
    for line in lines:
        if not line.startswith(">"):
            quote = False
        if not line.startswith("- "):
            unordered_list = False
        if not re.match(r'^\d+\.\s',line):
            ordered_list = False
    if quote:
        return BlockType.QUOTE
    if unordered_list:
        return BlockType.ULIST
    if ordered_list:
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        htmlnode = block_to_html_node(block)
        children.append(htmlnode)
    return ParentNode("div",children)


def block_to_html_node(block):
    blocktype = block_to_block_type(block)
    if blocktype ==BlockType.CODE:
        return code_to_html_node(block)
    elif blocktype==BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif blocktype==BlockType.HEADING:
        return heading_to_html_node(block)
    elif blocktype==BlockType.QUOTE:
        return quote_to_html_node(block)
    elif blocktype==BlockType.ULIST:
        return ulist_to_html_node(block)
    elif blocktype==BlockType.OLIST:
        return olist_to_html_node(block)


def text_to_children(text):
    text_node = text_to_textnodes(text)
    children =[]
    for node in text_node:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text,TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code",[child])
    return ParentNode("pre",[code])

def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p",children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    items = block.split("\n")
    list_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li",children))
    return ParentNode("ul",list_items)

def olist_to_html_node(block):
    items = block.split("\n")
    list_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        list_items.append(ParentNode("li",children))
    return ParentNode("ol",list_items)