import unittest
from helper_functions import *
from textnode import TextNode
from leafnode import LeafNode  


class TestTextNodeToHtmlNode(unittest.TestCase):
    
    def test_text_node(self):
        """Test text node without a tag."""
        node = TextNode("Just some text.", "text")
        html_node = text_node_to_html_node(node)
        expected_node = LeafNode(None, "Just some text.")
        self.assertEqual(repr(html_node), repr(expected_node))
    
    def test_bold_node(self):
        """Test bold text node."""
        node = TextNode("Bold text", "bold")
        html_node = text_node_to_html_node(node)
        expected_node = LeafNode("b", "Bold text")
        self.assertEqual(repr(html_node), repr(expected_node))
    
    def test_italic_node(self):
        """Test italic text node."""
        node = TextNode("Italic text", "italic")
        html_node = text_node_to_html_node(node)
        expected_node = LeafNode("i", "Italic text")
        self.assertEqual(repr(html_node), repr(expected_node))
    
    def test_code_node(self):
        """Test code text node."""
        node = TextNode("print('Hello World')", "code")
        html_node = text_node_to_html_node(node)
        expected_node = LeafNode("code", "print('Hello World')")
        self.assertEqual(repr(html_node), repr(expected_node))
    
    def test_link_node(self):
        """Test link text node with URL."""
        node = TextNode("Click here", "link", "https://www.example.com")
        html_node = text_node_to_html_node(node)
        expected_node = LeafNode("a", "Click here", {"href": "https://www.example.com"})
        self.assertEqual(repr(html_node), repr(expected_node))
    
    def test_image_node(self):
        """Test image node with URL and alt text."""
        node = TextNode("Example image", "image", "https://www.example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        expected_node = LeafNode("img", "", {"src": "https://www.example.com/image.jpg", "alt": "Example image"})
        self.assertEqual(repr(html_node), repr(expected_node))
    
    def test_invalid_text_type(self):
        """Test invalid text type, should raise an exception."""
        node = TextNode("Invalid text", "invalid")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
    
    def test_link_node_missing_url(self):
        """Test link node without URL, should raise an exception."""
        node = TextNode("Click here", "link")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
    
    def test_image_node_missing_url(self):
        """Test image node without URL, should raise an exception."""
        node = TextNode("Example image", "image")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
            
class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_single_split(self):
        """Test a single occurrence of the delimiter."""
        node = TextNode("This is `code` inside text", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(" inside text", "text")
        ]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])

    def test_multiple_splits(self):
        """Test multiple occurrences of the delimiter."""
        node = TextNode("This is `code` and `more code`", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(" and ", "text"),
            TextNode("more code", "code")
        ]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])
    
    def test_no_delimiter(self):
        """Test no delimiter in the text (should remain unchanged)."""
        node = TextNode("This is normal text without any delimiter", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        
        expected_nodes = [TextNode("This is normal text without any delimiter", "text")]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])

    def test_empty_text(self):
        """Test an empty text node."""
        node = TextNode("", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        
        expected_nodes = [TextNode("", "text")]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])
    
    def test_non_text_nodes(self):
        """Test that non-text nodes are left intact."""
        node = TextNode("This is text", "bold")  # Non-text node (e.g., bold)
        new_nodes = split_nodes_delimiter([node], "`", "code")
        
        expected_nodes = [TextNode("This is text", "bold")]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])

    def test_complex_text(self):
        """Test a complex text with multiple delimiters and normal text."""
        node = TextNode("Here is `code`, more text, and `another code` block", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        
        expected_nodes = [
            TextNode("Here is ", "text"),
            TextNode("code", "code"),
            TextNode(", more text, and ", "text"),
            TextNode("another code", "code"),
            TextNode(" block", "text")
        ]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])
        
class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_single_image(self):
        """Test extraction of a single image from Markdown."""
        text = "This is an image: ![Alt text](https://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("Alt text", "https://example.com/image.png")]
        self.assertEqual(result, expected)
    
    def test_extract_multiple_images(self):
        """Test extraction of multiple images from Markdown."""
        text = "![Alt1](https://example.com/img1.png) and ![Alt2](https://example.com/img2.png)"
        result = extract_markdown_images(text)
        expected = [
            ("Alt1", "https://example.com/img1.png"),
            ("Alt2", "https://example.com/img2.png")
        ]
        self.assertEqual(result, expected)

    def test_extract_image_with_no_alt_text(self):
        """Test extraction of an image with no alt text."""
        text = "This is an image: ![](https://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("", "https://example.com/image.png")]
        self.assertEqual(result, expected)

    def test_no_image_found(self):
        """Test when there are no images in the text."""
        text = "This is just text with no images."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

    def test_extract_single_link(self):
        """Test extraction of a single link from Markdown."""
        text = "This is a link: [Example](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("Example", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_multiple_links(self):
        """Test extraction of multiple links from Markdown."""
        text = "[Google](https://google.com) and [Bing](https://bing.com)"
        result = extract_markdown_links(text)
        expected = [
            ("Google", "https://google.com"),
            ("Bing", "https://bing.com")
        ]
        self.assertEqual(result, expected)

    def test_extract_link_with_no_text(self):
        """Test extraction of a link with no display text."""
        text = "This is a link: [](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("", "https://example.com")]
        self.assertEqual(result, expected)

    def test_no_link_found(self):
        """Test when there are no links in the text."""
        text = "This is just text with no links."
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

    def test_ignore_images_for_links(self):
        """Ensure that images are not mistaken for links in the link extractor."""
        text = "This is an image: ![Alt text](https://example.com/image.png)"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)
        
class TestSplitNodesLink(unittest.TestCase):

    def test_single_link(self):
        """Test splitting a single link in the text."""
        node = TextNode("This is a [link](https://example.com)", "text")
        new_nodes = split_nodes_link([node])
        
        expected_nodes = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com")
        ]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])

    def test_multiple_links(self):
        """Test splitting multiple links in the text."""
        node = TextNode("Here is a [link1](https://example1.com) and [link2](https://example2.com)", "text")
        new_nodes = split_nodes_link([node])
        
        expected_nodes = [
            TextNode("Here is a ", "text"),
            TextNode("link1", "link", "https://example1.com"),
            TextNode(" and ", "text"),
            TextNode("link2", "link", "https://example2.com")
        ]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])

    def test_no_links(self):
        """Test when there are no links in the text."""
        node = TextNode("This is just text without any links", "text")
        new_nodes = split_nodes_link([node])
        
        expected_nodes = [TextNode("This is just text without any links", "text")]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])

    def test_non_text_node(self):
        """Test that non-text nodes remain unchanged."""
        node = TextNode("This is bold text", "bold")  # Non-text node (e.g., bold)
        new_nodes = split_nodes_link([node])
        
        expected_nodes = [TextNode("This is bold text", "bold")]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])


class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        """Test splitting a single image in the text."""
        node = TextNode("Here is an image: ![Alt text](https://example.com/image.png)", "text")
        new_nodes = split_nodes_image([node])
        
        expected_nodes = [
            TextNode("Here is an image: ", "text"),
            TextNode("Alt text", "image", "https://example.com/image.png")
        ]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])

    def test_multiple_images(self):
        """Test splitting multiple images in the text."""
        node = TextNode("Here is ![image1](https://example1.com) and ![image2](https://example2.com)", "text")
        new_nodes = split_nodes_image([node])
        
        expected_nodes = [
            TextNode("Here is ", "text"),
            TextNode("image1", "image", "https://example1.com"),
            TextNode(" and ", "text"),
            TextNode("image2", "image", "https://example2.com")
        ]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])

    def test_no_images(self):
        """Test when there are no images in the text."""
        node = TextNode("This is just text without any images", "text")
        new_nodes = split_nodes_image([node])
        
        expected_nodes = [TextNode("This is just text without any images", "text")]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])

    def test_non_text_node(self):
        """Test that non-text nodes remain unchanged."""
        node = TextNode("This is italic text", "italic")  # Non-text node (e.g., italic)
        new_nodes = split_nodes_image([node])
        
        expected_nodes = [TextNode("This is italic text", "italic")]
        
        self.assertEqual([repr(n) for n in new_nodes], [repr(n) for n in expected_nodes])
        
class TestTextToTextNodes(unittest.TestCase):
    
    def test_text_only(self):
        """Test text with no formatting."""
        text = "This is a plain text with no formatting."
        nodes = text_to_textnodes(text)
        
        expected_nodes = [TextNode("This is a plain text with no formatting.", "text")]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])
    
    def test_bold_text(self):
        """Test text with bold formatting."""
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text.", "text")
        ]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])

    def test_italic_text(self):
        """Test text with italic formatting."""
        text = "This is *italic* text."
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text.", "text")
        ]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])

    def test_code_text(self):
        """Test text with inline code."""
        text = "This is `code` text."
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(" text.", "text")
        ]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])
    
    def test_link_in_text(self):
        """Test text with a single link."""
        text = "This is a [link](https://example.com)."
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(".", "text")
        ]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])

    def test_image_in_text(self):
        """Test text with a single image."""
        text = "Here is an ![image](https://example.com/image.png)."
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("Here is an ", "text"),
            TextNode("image", "image", "https://example.com/image.png"),
            TextNode(".", "text")
        ]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])

    def test_combined_formatting(self):
        """Test text with bold, italic, code, link, and image formatting combined."""
        text = "This is **bold**, *italic*, `code`, a [link](https://example.com), and an ![image](https://example.com/image.png)."
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(", ", "text"),
            TextNode("italic", "italic"),
            TextNode(", ", "text"),
            TextNode("code", "code"),
            TextNode(", a ", "text"),
            TextNode("link", "link", "https://example.com"),
            TextNode(", and an ", "text"),
            TextNode("image", "image", "https://example.com/image.png"),
            TextNode(".", "text")
        ]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])

    def test_no_formatting(self):
        """Test text with no formatting (plain text)."""
        text = "Just plain text."
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("Just plain text.", "text")
        ]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])

    def test_empty_text(self):
        """Test an empty string."""
        text = ""
        nodes = text_to_textnodes(text)
        
        expected_nodes = []
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])
    
    def test_text_with_only_link(self):
        """Test text with only a link."""
        text = "[Example](https://example.com)"
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("Example", "link", "https://example.com")
        ]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])
    
    def test_text_with_only_image(self):
        """Test text with only an image."""
        text = "![Alt text](https://example.com/image.png)"
        nodes = text_to_textnodes(text)
        
        expected_nodes = [
            TextNode("Alt text", "image", "https://example.com/image.png")
        ]
        
        self.assertEqual([repr(n) for n in nodes], [repr(n) for n in expected_nodes])
        
class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_single_block(self):
        """Test Markdown with a single block."""
        markdown = "# This is a heading"
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a heading"]
        self.assertEqual(blocks, expected)
    
    def test_multiple_blocks(self):
        """Test Markdown with multiple blocks."""
        markdown = "# Heading\n\nThis is a paragraph.\n\nAnother paragraph."
        blocks = markdown_to_blocks(markdown)
        expected = ["# Heading", "This is a paragraph.", "Another paragraph."]
        self.assertEqual(blocks, expected)
    
    def test_trailing_whitespace(self):
        """Test Markdown with trailing whitespace in blocks."""
        markdown = "# Heading \n\n This is a paragraph. \n\n  Another paragraph.  "
        blocks = markdown_to_blocks(markdown)
        expected = ["# Heading", "This is a paragraph.", "Another paragraph."]
        self.assertEqual(blocks, expected)
    
    def test_excessive_newlines(self):
        """Test Markdown with excessive newlines between blocks."""
        markdown = "# Heading\n\n\n\nThis is a paragraph.\n\n\n\nAnother paragraph."
        blocks = markdown_to_blocks(markdown)
        expected = ["# Heading", "This is a paragraph.", "Another paragraph."]
        self.assertEqual(blocks, expected)
    
    def test_only_newlines(self):
        """Test Markdown that only contains newlines."""
        markdown = "\n\n\n\n"
        blocks = markdown_to_blocks(markdown)
        expected = []
        self.assertEqual(blocks, expected)
    
    def test_empty_input(self):
        """Test Markdown that is completely empty."""
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        expected = []
        self.assertEqual(blocks, expected)
    
    def test_whitespace_only_blocks(self):
        """Test Markdown with whitespace-only blocks."""
        markdown = "   \n\n\n\n   \n\nAnother paragraph."
        blocks = markdown_to_blocks(markdown)
        expected = ["Another paragraph."]
        self.assertEqual(blocks, expected)
    
    def test_list_items(self):
        """Test Markdown with list items (blocks without extra newlines)."""
        markdown = "- Item 1\n- Item 2\n\nAnother block."
        blocks = markdown_to_blocks(markdown)
        expected = ['- Item 1\n- Item 2', 'Another block.']
        self.assertEqual(blocks, expected)

    def test_code_block(self):
        """Test Markdown with a code block."""
        markdown = "Here is a paragraph.\n\n```\nCode block\nwith multiple lines\n```"
        blocks = markdown_to_blocks(markdown)
        expected = ["Here is a paragraph.", "```\nCode block\nwith multiple lines\n```"]
        self.assertEqual(blocks, expected)
    
    def test_mixed_content(self):
        """Test Markdown with mixed content including headers, paragraphs, and code."""
        markdown = "# Heading 1\n\nParagraph 1.\n\n## Heading 2\n\n```\nCode block\n```"
        blocks = markdown_to_blocks(markdown)
        expected = ['# Heading 1', 'Paragraph 1.', '## Heading 2', '```\nCode block\n```']
        self.assertEqual(blocks, expected)
        
class TestBlockToBlockType(unittest.TestCase):
    
    def test_heading_1(self):
        """Test a level 1 heading."""
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), "heading-1")

    def test_heading_2(self):
        """Test a level 2 heading."""
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), "heading-2")
    
    def test_heading_6(self):
        """Test a level 6 heading."""
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), "heading-6")
    
    def test_code_block(self):
        """Test a code block."""
        block = "```\nCode block\nwith multiple lines\n```"
        self.assertEqual(block_to_block_type(block), "code")
    
    def test_quote_block(self):
        """Test a quote block."""
        block = "> This is a quote\n> Another line of quote"
        self.assertEqual(block_to_block_type(block), "quote")
    
    def test_unordered_list(self):
        """Test an unordered list block with * and -."""
        block = "* Item 1\n* Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), "unordered-list")

    def test_ordered_list(self):
        """Test an ordered list block with increasing numbers."""
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), "ordered-list")

    def test_ordered_list_with_incorrect_numbers(self):
        """Test an ordered list block with incorrect numbering (should not be an ordered list)."""
        block = "1. First item\n3. Second item\n4. Third item"
        self.assertEqual(block_to_block_type(block), "paragraph")
    
    def test_paragraph(self):
        """Test a paragraph block."""
        block = "This is a regular paragraph."
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_mixed_unordered_list(self):
        """Test a mixed unordered list with both * and -."""
        block = "* First item\n- Second item"
        self.assertEqual(block_to_block_type(block), "unordered-list")
    
    def test_mixed_ordered_list_invalid(self):
        """Test an invalid ordered list where the numbering doesn't increment correctly."""
        block = "1. First item\n3. Second item"
        self.assertEqual(block_to_block_type(block), "paragraph")
    
    def test_empty_block(self):
        """Test an empty block (should be treated as a paragraph)."""
        block = ""
        self.assertEqual(block_to_block_type(block), "paragraph")
        
class TestMarkdownToHtmlNode(unittest.TestCase):
    
    def test_heading(self):
        """Test markdown with different headings."""
        markdown = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<h1>Heading 1</h1>"
            "<h2>Heading 2</h2>"
            "<h3>Heading 3</h3>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_paragraph(self):
        """Test markdown with a single paragraph."""
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<p>This is a paragraph.</p>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_bold_and_italic(self):
        """Test markdown with bold and italic text."""
        markdown = "This is **bold** and *italic*."
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<p>This is <b>bold</b> and <i>italic</i>.</p>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_code_block(self):
        """Test markdown with a code block."""
        markdown = "```\nCode block\n```"
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<pre>Code block</pre>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_link(self):
        """Test markdown with a link."""
        markdown = "This is a [link](https://example.com)."
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<p>This is a <a href=\"https://example.com\">link</a>.</p>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_image(self):
        """Test markdown with an image."""
        markdown = "This is an image: ![Alt text](https://example.com/image.png)"
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<p>This is an image: <img src=\"https://example.com/image.png\" alt=\"Alt text\"></img></p>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_quote_block(self):
        """Test markdown with a quote block."""
        markdown = "> This is a quote."
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<blockquote>This is a quote.</blockquote>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_unordered_list(self):
        """Test markdown with an unordered list."""
        markdown = "* Item 1\n* Item 2\n* Item 3"
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<ul>"
            "<li>Item 1</li>"
            "<li>Item 2</li>"
            "<li>Item 3</li>"
            "</ul>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_ordered_list(self):
        """Test markdown with an ordered list."""
        markdown = "1. First item\n2. Second item\n3. Third item"
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<ol>"
            "<li>First item</li>"
            "<li>Second item</li>"
            "<li>Third item</li>"
            "</ol>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)

    def test_combined_content(self):
        self.maxDiff = None
        """Test markdown with headings, paragraphs, and lists."""
        markdown = (
            "# Heading 1\n\n"
            "This is a paragraph with **bold** and *italic* text.\n\n"
            "1. First item\n2. Second item\n\n"
            "> A quote\n\n"
            "![Image](https://example.com/image.png)\n\n"
            "```\nCode block\n```"
        )
        html_node = markdown_to_html_node(markdown)
        
        expected_html = (
            "<div>"
            "<h1>Heading 1</h1>"
            "<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>"
            "<ol>"
            "<li>First item</li>"
            "<li>Second item</li>"
            "</ol>"
            "<blockquote>A quote</blockquote>"
            "<p><img src=\"https://example.com/image.png\" alt=\"Image\"></img></p>"
            "<pre>Code block</pre>"
            "</div>"
        )
        self.assertEqual(html_node.to_html(), expected_html)


class TestTextToChildren(unittest.TestCase):
    
    def test_bold_text(self):
        """Test inline bold text conversion."""
        text = "This is **bold**."
        children = text_to_children(text)
        
        expected_html = "This is <b>bold</b>."
        self.assertEqual("".join([node.to_html() for node in children]), expected_html)

    def test_italic_text(self):
        """Test inline italic text conversion."""
        text = "This is *italic*."
        children = text_to_children(text)
        
        expected_html = "This is <i>italic</i>."
        self.assertEqual("".join([node.to_html() for node in children]), expected_html)

    def test_link_text(self):
        """Test inline link text conversion."""
        text = "This is a [link](https://example.com)."
        children = text_to_children(text)
        
        expected_html = "This is a <a href=\"https://example.com\">link</a>."
        self.assertEqual("".join([node.to_html() for node in children]), expected_html)

    def test_code_text(self):
        """Test inline code text conversion."""
        text = "This is `code`."
        children = text_to_children(text)
        
        expected_html = "This is <code>code</code>."
        self.assertEqual("".join([node.to_html() for node in children]), expected_html)

    def test_image_text(self):
        """Test inline image conversion."""
        text = "Here is an image: ![Alt text](https://example.com/image.png)"
        children = text_to_children(text)
        
        expected_html = "Here is an image: <img src=\"https://example.com/image.png\" alt=\"Alt text\"></img>"
        self.assertEqual("".join([node.to_html() for node in children]), expected_html)


class TestExtractTitle(unittest.TestCase):
    
    def test_valid_title(self):
        """Test that a valid title is correctly extracted."""
        markdown = "# My Awesome Document\n\nThis is the rest of the document."
        self.assertEqual(extract_title(markdown), "My Awesome Document")

    def test_title_with_trailing_whitespace(self):
        """Test that a title with trailing whitespace is correctly stripped."""
        markdown = "# My Awesome Document   \n\nThis is the rest of the document."
        self.assertEqual(extract_title(markdown), "My Awesome Document")
    
    def test_no_title(self):
        """Test that an exception is raised when there is no title."""
        markdown = "This is a document without a title."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Document must have a header.")
    
    def test_title_with_extra_hashes(self):
        """Test that a title with multiple hashes is extracted correctly (e.g., `### Title`)."""
        markdown = "### Subheading Title\n\nThis is a subheading, not a title."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Document must have a header.")
    
    def test_empty_document(self):
        """Test that an exception is raised when the document is empty."""
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Document must have a header.")

    def test_title_in_first_line_only(self):
        """Test that a title is only extracted from the first line of the document."""
        markdown = "# My First Title\n## Subtitle\n\nContent of the document."
        self.assertEqual(extract_title(markdown), "My First Title")
    
    def test_title_with_special_characters(self):
        """Test that a title with special characters is correctly extracted."""
        markdown = "# Title with @#$%^&*() special characters\n\nThis is the rest of the document."
        self.assertEqual(extract_title(markdown), "Title with @#$%^&*() special characters")

if __name__ == '__main__':
    unittest.main()
