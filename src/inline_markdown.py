from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result =[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        lines = node.text.split(delimiter)
        if len(lines) % 2 != 1:
            raise Exception("Invalid Markdown")
        for x in range(len(lines)):
            if lines[x] == "":
                continue
            if x % 2 ==0:
                current_node = TextNode(lines[x],TextType.TEXT,None)
                result.append(current_node)
            else:
                current_node = TextNode(lines[x],text_type,None)
                result.append(current_node)
    return result


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    result = []
    for alt_text, link in matches:
        result.append((alt_text, link))
    return result

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    result = []
    for alt_text, link in matches:
        result.append((alt_text, link))
    return result

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        list_images = extract_markdown_images(old_node.text)
        if len(list_images) == 0:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        for i in range(len(list_images)):
            image_alt = list_images[i][0]
            image_link = list_images[i][1]
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image_alt,
                    TextType.IMAGE,
                    image_link,
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        list_links = extract_markdown_links(original_text)
        if len(list_links) == 0:
            new_nodes.append(old_node)
            continue
        for i in range(len(list_links)):
            image_alt = list_links[i][0]
            image_link = list_links[i][1]
            sections = original_text.split(f"[{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image_alt,
                    TextType.LINK,
                    image_link,
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    result = split_nodes_delimiter([TextNode(text,TextType.TEXT,None)],"**",TextType.BOLD)
    result = split_nodes_delimiter(result,"_",TextType.ITALIC)
    result = split_nodes_delimiter(result,"`",TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result
        