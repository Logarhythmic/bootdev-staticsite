import textnode
import htmlnode
import markdown

def main():
    node = htmlnode.LeafNode("a", "Example", props={"href": "http://example.com"})
    
    print(node)
    print(node.to_html())

    MDnode = textnode.TextNode("This is **bold** and this is *italic* and here is some `code`.", textnode.TextType.TEXT)
    print(markdown.split_nodes_delimiter([MDnode], "**", textnode.TextType.BOLD))

if __name__ == "__main__":
    main()