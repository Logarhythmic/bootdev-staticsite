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


if __name__ == "__main__":
    unittest.main()