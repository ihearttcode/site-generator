import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    
    def test_valid_leafnode(self):
        """Test creating a valid LeafNode with tag, value, and props."""
        leaf = LeafNode("p", "This is a paragraph.", {"class": "text"})
        self.assertEqual(leaf.tag, "p")
        self.assertEqual(leaf.value, "This is a paragraph.")
        self.assertEqual(leaf.props, {"class": "text"})
        self.assertIsNone(leaf.children)  # Ensure children is None
    
    def test_leafnode_no_value(self):
        """Test that creating a LeafNode without a value raises a ValueError."""
        with self.assertRaises(ValueError):
            LeafNode("p")
    
    def test_leafnode_no_children_allowed(self):
        """Test that LeafNode does not allow children."""
        leaf = LeafNode("div", "Leaf content")
        self.assertIsNone(leaf.children)  # Check that children is always None
    
    def test_props_to_html(self):
        """Test the props_to_html method of LeafNode."""
        leaf = LeafNode("a", "Click me", {"href": "https://www.google.com", "target": "_blank"})
        expected_props = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(leaf.props_to_html(), expected_props)

    def test_repr(self):
        """Test the __repr__ method for LeafNode."""
        leaf = LeafNode("span", "Leaf node", {"class": "leaf-class"})
        expected_repr = (
            "LeafNode(\n"
            "  tag='span',\n"
            "  value='Leaf node',\n"
            "  props={'class': 'leaf-class'}\n"
            ")"
        )
        self.assertEqual(repr(leaf), expected_repr)

if __name__ == '__main__':
    unittest.main()
