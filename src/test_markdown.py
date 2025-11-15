import unittest
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_split_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
    
    def test_split_multiple_delimiters(self):
        node = TextNode("Code `one` and `two` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Code ")
        self.assertEqual(new_nodes[1].text, "one")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "two")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " here")
    
    def test_split_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_split_unclosed_delimiter_raises_error(self):
        node = TextNode("This has `unclosed delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unclosed delimiter", str(context.exception))
    
    def test_split_non_text_node_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
    
    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("First `code` text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second `code` text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "First ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Already bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, "Second ")
        self.assertEqual(new_nodes[5].text, "code")
        self.assertEqual(new_nodes[5].text_type, TextType.CODE)
    
    def test_split_empty_between_delimiters(self):
        node = TextNode("Text `` empty", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # Should skip empty parts
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text, " empty")


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_single_image(self):
        text = "This is text with an ![image](https://example.com/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "image")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "https://example.com/image.png")
    
    def test_extract_multiple_images(self):
        text = "![first](https://example.com/1.png) and ![second](https://example.com/2.png)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "first")
        self.assertEqual(result[0].url, "https://example.com/1.png")
        self.assertEqual(result[1].text, "second")
        self.assertEqual(result[1].url, "https://example.com/2.png")
    
    def test_extract_image_with_empty_alt(self):
        text = "![](https://example.com/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].url, "https://example.com/image.png")
    
    def test_extract_no_images(self):
        text = "This is just plain text with no images"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 0)
    
    def test_extract_images_ignores_links(self):
        text = "![image](https://example.com/img.png) and [link](https://example.com)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "image")
    
    def test_extract_image_with_spaces_in_alt(self):
        text = "![alt text with spaces](https://example.com/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "alt text with spaces")


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_single_link(self):
        text = "This is text with a [link](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "link")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "https://example.com")
    
    def test_extract_multiple_links(self):
        text = "[first](https://example.com) and [second](https://boot.dev)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "first")
        self.assertEqual(result[0].url, "https://example.com")
        self.assertEqual(result[1].text, "second")
        self.assertEqual(result[1].url, "https://boot.dev")
    
    def test_extract_no_links(self):
        text = "This is just plain text with no links"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 0)
    
    def test_extract_links_ignores_images(self):
        text = "[link](https://example.com) and ![image](https://example.com/img.png)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "link")
    
    def test_extract_link_with_spaces(self):
        text = "[click here](https://example.com/page)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "click here")
    
    def test_extract_link_with_path(self):
        text = "[documentation](https://example.com/docs/guide.html)"
        result = extract_markdown_links(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].url, "https://example.com/docs/guide.html")


if __name__ == "__main__":
    unittest.main()
