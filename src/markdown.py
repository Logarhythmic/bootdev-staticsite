from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(text)
        
        if not images:
            new_nodes.append(node)
            continue
        
        for image in images:
            sections = text.split(f"![{image.text}]({image.url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(image)
            text = sections[1] if len(sections) > 1 else ""
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)
        
        if not links:
            new_nodes.append(node)
            continue
        
        for link in links:
            sections = text.split(f"[{link.text}]({link.url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(link)
            text = sections[1] if len(sections) > 1 else ""
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # Extract images and links first to avoid processing their URLs
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # Then process inline formatting
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block.strip():
            filtered_blocks.append(block.strip())
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    
    # Check for heading (1-6 # characters followed by space)
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with * or - followed by space)
    if all(line.startswith("* ") or line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (every line starts with number. followed by space, incrementing from 1)
    if all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH

def text_to_children(text):
    """Convert text with inline markdown to a list of HTMLNode children"""
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def text_node_to_html_node(text_node):
    """Convert a TextNode to an HTMLNode (LeafNode)"""
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")

def markdown_to_html_node(markdown):
    """Convert a full markdown document to a single parent HTMLNode"""
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            # Count the number of # characters
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            # Remove the # characters and space
            text = block[level:].strip()
            children_nodes = text_to_children(text)
            children.append(ParentNode(f"h{level}", children_nodes))
        
        elif block_type == BlockType.CODE:
            # Remove the ``` markers
            code_text = block.strip("`").strip()
            children.append(ParentNode("pre", [LeafNode("code", code_text)]))
        
        elif block_type == BlockType.QUOTE:
            # Remove > from each line
            lines = block.split("\n")
            quote_text = "\n".join(line[1:].strip() for line in lines)
            children_nodes = text_to_children(quote_text)
            children.append(ParentNode("blockquote", children_nodes))
        
        elif block_type == BlockType.UNORDERED_LIST:
            # Create list items
            lines = block.split("\n")
            list_items = []
            for line in lines:
                # Remove the marker (- or *)
                text = line[2:]
                item_children = text_to_children(text)
                list_items.append(ParentNode("li", item_children))
            children.append(ParentNode("ul", list_items))
        
        elif block_type == BlockType.ORDERED_LIST:
            # Create list items
            lines = block.split("\n")
            list_items = []
            for line in lines:
                # Remove the number and ". "
                text = line.split(". ", 1)[1]
                item_children = text_to_children(text)
                list_items.append(ParentNode("li", item_children))
            children.append(ParentNode("ol", list_items))
        
        else:  # PARAGRAPH
            children_nodes = text_to_children(block)
            children.append(ParentNode("p", children_nodes))
    
    return ParentNode("div", children)

def extract_title(markdown):
    """Extract the h1 title from a markdown document"""
    lines = markdown.strip().split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")
