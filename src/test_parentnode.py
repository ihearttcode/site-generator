import unittest
from parentnode import ParentNode
from leafnode import LeafNode  # Import LeafNode as it's used in the tests

class TestParentNode(unittest.TestCase):

    def test_valid_parentnode(self):
        """Test valid ParentNode with multiple children."""
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "More normal text"),
            ]
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>Italic text</i>More normal text</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_with_props(self):
        """Test ParentNode with props (e.g., class attribute)."""
        node = ParentNode(
            "div",
            [
                LeafNode(None, "Hello world!"),
            ],
            {"class": "container"}
        )
        expected_html = '<div class="container">Hello world!</div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_with_children_having_props(self):
        """Test ParentNode where children have props."""
        node = ParentNode(
            "ul",
            [
                LeafNode("li", "First item", {"class": "item"}),
                LeafNode("li", "Second item", {"class": "item"}),
            ]
        )
        expected_html = '<ul><li class="item">First item</li><li class="item">Second item</li></ul>'
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_no_tag(self):
        """Test ParentNode with no tag, which should raise a ValueError."""
        with self.assertRaises(ValueError):
            ParentNode(
                None,
                [LeafNode("span", "Content")]
            )

    def test_parentnode_no_children(self):
        """Test ParentNode with no children, which should raise a ValueError."""
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    def test_parentnode_empty_children(self):
        """Test ParentNode with an empty children list, which should raise a ValueError."""
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_parentnode_with_mixed_children(self):
        """Test ParentNode with children having a mix of tags and no tags."""
        node = ParentNode(
            "p",
            [
                LeafNode("strong", "Important text"),
                LeafNode(None, "Just some normal text."),
                LeafNode("em", "Emphasized text"),
            ]
        )
        expected_html = "<p><strong>Important text</strong>Just some normal text.<em>Emphasized text</em></p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_with_multiple_children(self):
        """Test ParentNode with multiple LeafNodes, ensuring all children are rendered correctly."""
        node = ParentNode(
            "section",
            [
                LeafNode("h1", "Title"),
                LeafNode("p", "This is a paragraph."),
                LeafNode("p", "This is another paragraph."),
            ]
        )
        expected_html = "<section><h1>Title</h1><p>This is a paragraph.</p><p>This is another paragraph.</p></section>"
        self.assertEqual(node.to_html(), expected_html)

if __name__ == '__main__':
    unittest.main()
