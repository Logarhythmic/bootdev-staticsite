import unittest
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, extract_title
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


class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode("Text with ![image](https://example.com/img.png) here", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/img.png")
        self.assertEqual(result[2].text, " here")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_split_multiple_images(self):
        node = TextNode("![first](url1.png) and ![second](url2.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "first")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[2].text, "second")
        self.assertEqual(result[2].text_type, TextType.IMAGE)
    
    def test_split_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just plain text")
    
    def test_split_non_text_node_unchanged(self):
        node = TextNode("Bold text", TextType.BOLD)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.BOLD)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_single_link(self):
        node = TextNode("Text with [link](https://example.com) here", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com")
        self.assertEqual(result[2].text, " here")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_split_multiple_links(self):
        node = TextNode("[first](url1.com) and [second](url2.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "first")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[2].text, "second")
        self.assertEqual(result[2].text_type, TextType.LINK)
    
    def test_split_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just plain text")
    
    def test_split_non_text_node_unchanged(self):
        node = TextNode("Bold text", TextType.BOLD)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.BOLD)


class TestTextToTextnodes(unittest.TestCase):
    def test_full_markdown_conversion(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        self.assertEqual(len(result), len(expected))
        for i, (res, exp) in enumerate(zip(result, expected)):
            self.assertEqual(res.text, exp.text, f"Node {i} text mismatch")
            self.assertEqual(res.text_type, exp.text_type, f"Node {i} type mismatch")
            self.assertEqual(res.url, exp.url, f"Node {i} url mismatch")
    
    def test_only_bold(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
    
    def test_only_italic_asterisk(self):
        text = "This is *italic* text"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
    
    def test_only_italic_underscore(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
    
    def test_only_code(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
    
    def test_plain_text(self):
        text = "Just plain text with no markdown"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, text)
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_multiple_formatting_same_type(self):
        text = "**bold1** and **bold2**"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "bold1")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[2].text, "bold2")
        self.assertEqual(result[2].text_type, TextType.BOLD)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_standard(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(blocks[1], "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.")
        self.assertEqual(blocks[2], "- This is the first list item in a list block\n- This is a list item\n- This is another list item")
    
    def test_markdown_to_blocks_extra_newlines(self):
        markdown = """Block 1


Block 2"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "Block 1")
        self.assertEqual(blocks[1], "Block 2")
    
    def test_markdown_to_blocks_with_whitespace(self):
        markdown = """  Block 1  

  Block 2  """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "Block 1")
        self.assertEqual(blocks[1], "Block 2")
    
    def test_markdown_to_blocks_single_block(self):
        markdown = "Just one block of text"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "Just one block of text")
    
    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 0)
    
    def test_markdown_to_blocks_only_whitespace(self):
        markdown = "   \n\n   "
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 0)
    
    def test_markdown_to_blocks_multiple_blank_lines(self):
        markdown = """Block 1


Block 2



Block 3"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "Block 1")
        self.assertEqual(blocks[1], "Block 2")
        self.assertEqual(blocks[2], "Block 3")


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_level_1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_level_2(self):
        block = "## This is a heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_level_6(self):
        block = "###### This is a heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_no_space_not_heading(self):
        block = "#Not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_single_line(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_multiple_lines(self):
        block = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_all_lines_must_start_with_gt(self):
        block = "> Line 1\nNot a quote\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_dash(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_asterisk(self):
        block = "* Item 1\n* Item 2\n* Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_mixed_valid(self):
        block = "- Item 1\n* Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_needs_space(self):
        block = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_must_start_at_1(self):
        block = "2. First\n3. Second\n4. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_must_increment(self):
        block = "1. First\n1. Second\n1. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_must_be_sequential(self):
        block = "1. First\n2. Second\n4. Fourth"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_simple(self):
        block = "This is just a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nof text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_with_markdown(self):
        block = "This has **bold** and *italic* text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is a paragraph."
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<p>This is a paragraph.</p>", html)
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue(html.endswith("</div>"))
    
    def test_paragraph_with_inline_markdown(self):
        markdown = "This is **bold** and *italic* text."
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
    
    def test_heading_levels(self):
        markdown = """# Heading 1

## Heading 2

### Heading 3"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<h1>Heading 1</h1>", html)
        self.assertIn("<h2>Heading 2</h2>", html)
        self.assertIn("<h3>Heading 3</h3>", html)
    
    def test_heading_with_inline_markdown(self):
        markdown = "# This is **bold** heading"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<h1>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("</h1>", html)
    
    def test_code_block(self):
        markdown = "```\ndef hello():\n    print('world')\n```"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<pre><code>", html)
        self.assertIn("def hello():", html)
        self.assertIn("</code></pre>", html)
    
    def test_quote(self):
        markdown = "> This is a quote\n> with multiple lines"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<blockquote>", html)
        self.assertIn("This is a quote", html)
        self.assertIn("with multiple lines", html)
        self.assertIn("</blockquote>", html)
    
    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<ul>", html)
        self.assertIn("<li>Item 1</li>", html)
        self.assertIn("<li>Item 2</li>", html)
        self.assertIn("<li>Item 3</li>", html)
        self.assertIn("</ul>", html)
    
    def test_ordered_list(self):
        markdown = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<ol>", html)
        self.assertIn("<li>First</li>", html)
        self.assertIn("<li>Second</li>", html)
        self.assertIn("<li>Third</li>", html)
        self.assertIn("</ol>", html)
    
    def test_list_with_inline_markdown(self):
        markdown = "- Item with **bold**\n- Item with *italic*"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
    
    def test_multiple_blocks(self):
        markdown = """# Heading

This is a paragraph.

- List item 1
- List item 2"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<h1>Heading</h1>", html)
        self.assertIn("<p>This is a paragraph.</p>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<li>List item 1</li>", html)
    
    def test_complex_document(self):
        markdown = """# Welcome

This is **bold** and `code`.

## Section

> A quote here

1. First item
2. Second item"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        
        # Check all elements are present
        self.assertIn("<h1>Welcome</h1>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn("<h2>Section</h2>", html)
        self.assertIn("<blockquote>", html)
        self.assertIn("<ol>", html)
        
        # Verify it's wrapped in a div
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue(html.endswith("</div>"))
    
    def test_paragraph_with_link(self):
        markdown = "Check out [this link](https://example.com)"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn('<a href="https://example.com">this link</a>', html)
    
    def test_paragraph_with_image(self):
        markdown = "Here is an image: ![alt text](https://example.com/img.png)"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn('<img src="https://example.com/img.png" alt="alt text"', html)


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")
    
    def test_extract_title_with_extra_whitespace(self):
        markdown = "#  Title with spaces  "
        self.assertEqual(extract_title(markdown), "Title with spaces")
    
    def test_extract_title_with_other_content(self):
        markdown = """# Main Title

This is a paragraph.

## Sub heading"""
        self.assertEqual(extract_title(markdown), "Main Title")
    
    def test_extract_title_no_h1_raises_error(self):
        markdown = "## Only h2 here"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_extract_title_empty_raises_error(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_extract_title_with_leading_content(self):
        markdown = """Some text

# The Title

More content"""
        self.assertEqual(extract_title(markdown), "The Title")


if __name__ == "__main__":
    unittest.main()
