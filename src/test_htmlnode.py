import unittest
import htmlnode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = htmlnode.HTMLNode("<div>This is a div</div>", htmlnode.HTMLTags.DIV)
        node2 = htmlnode.HTMLNode("<div>This is a div</div>", htmlnode.HTMLTags.DIV)
        node3 = htmlnode.HTMLNode("<span>This is a span</span>", htmlnode.HTMLTags.SPAN)
        node4 = htmlnode.HTMLNode("<div>This is a div</div>", htmlnode.HTMLTags.P)
        node5 = htmlnode.HTMLNode()
        #node5 = htmlnode.HTMLNode("<div>This is a div</div>", htmlnode.HTMLTags.DIV, id="main-div")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertEqual(node5.children, [])
        self.assertEqual(node5.props, {})
        self.assertEqual(node5.tag, None)
        self.assertEqual(node5.value, None)
        #self.assertEqual(node.id, None)
        #self.assertNotEqual(node5.id, node.id)

if __name__ == "__main__":
    unittest.main()