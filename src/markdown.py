from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown: unclosed delimiter '{delimiter}'")
        
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                # Outside delimiter - keep original text type
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Inside delimiter - apply new text type
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    image_nodes = []
    for alt_text, url in matches:
        image_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
    return image_nodes

def extract_markdown_links(text):
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    link_nodes = []
    for link_text, url in matches:
        link_nodes.append(TextNode(link_text, TextType.LINK, url))
    return link_nodes

