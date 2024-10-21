import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_no_props(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_empty_props(self):
        node = HTMLNode(props={})
        expected_output = ''
        self.assertEqual(node.props_to_html(), expected_output)

    def test_repr(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.google.com"})
        expected_output = (
            "HTMLNode(\n"
            "  tag='a',\n"
            "  value='Click here',\n"
            "  children=None,\n"
            "  props={'href': 'https://www.google.com'}\n"
            ")"
        )
        self.assertEqual(repr(node), expected_output)

if __name__ == '__main__':
    unittest.main()