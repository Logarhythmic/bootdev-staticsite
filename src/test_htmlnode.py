import unittest
import htmlnode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node1 = htmlnode.HTMLNode("div", "Hello")
        node2 = htmlnode.HTMLNode("div", "Hello")
        node3 = htmlnode.HTMLNode("span", "Hello")
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
    
    def test_eq_with_props(self):
        node1 = htmlnode.HTMLNode("a", "Link", None, {"href": "https://example.com"})
        node2 = htmlnode.HTMLNode("a", "Link", None, {"href": "https://example.com"})
        node3 = htmlnode.HTMLNode("a", "Link", None, {"href": "https://different.com"})
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
    
    def test_eq_with_children(self):
        child1 = htmlnode.HTMLNode("span", "child")
        child2 = htmlnode.HTMLNode("span", "child")
        node1 = htmlnode.HTMLNode("div", None, [child1])
        node2 = htmlnode.HTMLNode("div", None, [child2])
        self.assertEqual(node1, node2)
    
    def test_defaults(self):
        node = htmlnode.HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
    
    def test_props_to_html(self):
        node = htmlnode.HTMLNode("a", "Link", None, {"href": "https://example.com", "target": "_blank"})
        props_html = node.props_to_html()
        self.assertIn("href=\"https://example.com\"", props_html)
        self.assertIn("target=\"_blank\"", props_html)
        self.assertTrue(props_html.startswith(" "))
    
    def test_props_to_html_empty(self):
        node = htmlnode.HTMLNode("p", "Text")
        self.assertEqual(node.props_to_html(), "")
    
    def test_to_html_not_implemented(self):
        node = htmlnode.HTMLNode("div", "Test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = htmlnode.LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")
    
    def test_to_html_with_tag(self):
        node = htmlnode.LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")
    
    def test_to_html_with_props(self):
        node = htmlnode.LeafNode("a", "Click me", {"href": "https://example.com", "target": "_blank"})
        html = node.to_html()
        self.assertIn("<a", html)
        self.assertIn("href=\"https://example.com\"", html)
        self.assertIn("target=\"_blank\"", html)
        self.assertIn(">Click me</a>", html)
    
    def test_to_html_no_value_raises_error(self):
        node = htmlnode.LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_eq(self):
        node1 = htmlnode.LeafNode("p", "Hello")
        node2 = htmlnode.LeafNode("p", "Hello")
        node3 = htmlnode.LeafNode("p", "World")
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        node = htmlnode.ParentNode(
            "p",
            [
                htmlnode.LeafNode("b", "Bold text"),
                htmlnode.LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text</p>")
    
    def test_to_html_with_nested_parents(self):
        node = htmlnode.ParentNode(
            "div",
            [
                htmlnode.ParentNode(
                    "p",
                    [htmlnode.LeafNode("b", "Bold")],
                ),
                htmlnode.LeafNode("span", "Text"),
            ],
        )
        self.assertEqual(node.to_html(), "<div><p><b>Bold</b></p><span>Text</span></div>")
    
    def test_to_html_with_props(self):
        node = htmlnode.ParentNode(
            "div",
            [htmlnode.LeafNode("p", "Test")],
            {"class": "container", "id": "main"},
        )
        html = node.to_html()
        self.assertIn("<div", html)
        self.assertIn("class=\"container\"", html)
        self.assertIn("id=\"main\"", html)
        self.assertIn("><p>Test</p></div>", html)
    
    def test_to_html_no_tag_raises_error(self):
        node = htmlnode.ParentNode(None, [htmlnode.LeafNode("p", "Test")])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("tag", str(context.exception).lower())
    
    def test_to_html_no_children_raises_error(self):
        node = htmlnode.ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("children", str(context.exception).lower())
    
    def test_to_html_multiple_children(self):
        node = htmlnode.ParentNode(
            "p",
            [
                htmlnode.LeafNode("b", "Bold text"),
                htmlnode.LeafNode(None, "Normal text"),
                htmlnode.LeafNode("i", "italic text"),
                htmlnode.LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
    
    def test_eq(self):
        node1 = htmlnode.ParentNode("div", [htmlnode.LeafNode("p", "Test")])
        node2 = htmlnode.ParentNode("div", [htmlnode.LeafNode("p", "Test")])
        node3 = htmlnode.ParentNode("div", [htmlnode.LeafNode("p", "Different")])
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

if __name__ == "__main__":
    unittest.main()