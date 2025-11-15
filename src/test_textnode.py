import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("Different text", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.UNDERLINE)
        node5 = TextNode("This is a text node", TextType.BOLD, url="http://example.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertEqual(node.url, None)
        self.assertNotEqual(node5.url, node.url)
    
    def test_text_node_to_html_node_text(self):
        node = TextNode("Plain text", TextType.TEXT)
        self.assertEqual(node.text_node_to_html_node(), "Plain text")
    
    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        self.assertEqual(node.text_node_to_html_node(), "<b>Bold text</b>")
    
    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        self.assertEqual(node.text_node_to_html_node(), "<i>Italic text</i>")
    
    def test_text_node_to_html_node_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        self.assertEqual(node.text_node_to_html_node(), "<code>print('hello')</code>")
    
    def test_text_node_to_html_node_underline(self):
        node = TextNode("Underlined", TextType.UNDERLINE)
        self.assertEqual(node.text_node_to_html_node(), "<u>Underlined</u>")
    
    def test_text_node_to_html_node_link(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node.text_node_to_html_node(), '<a href="https://example.com">Click here</a>')
    
    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        self.assertEqual(node.text_node_to_html_node(), '<img src="https://example.com/image.png" alt="Image"/>')


if __name__ == "__main__":
    unittest.main()