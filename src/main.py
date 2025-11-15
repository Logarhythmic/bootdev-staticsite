import textnode
import htmlnode

def main():
    node = textnode.TextNode("Hello, world!", textnode.TextType.BOLD)
    print(node)

if __name__ == "__main__":
    main()