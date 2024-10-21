import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        
    def test_text_eq(self):
        node = TextNode("This is equal", "italic")
        node2 = TextNode("This is equal", "bold")
        self.assertEqual(node.text, node2.text)
    
    def test_text_type_eq(self):
        node = TextNode("This is some text", "bold", "https://boot.dev")
        node2 = TextNode("This is also some text", "bold", None)
        self.assertEqual(node.text_type, node2.text_type)
    
        
    def test_url_eq(self):
        node = TextNode("This is some text", "bold", "https://boot.dev")
        node2 = TextNode("This is also some text", "italics", "https://boot.dev")
        self.assertEqual(node.url, node2.url)
        
    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a test text node", "bold")
        self.assertNotEqual(node, node2)
        
    def test_text_not_eq(self):
        node = TextNode("This is equal", "italic")
        node2 = TextNode("This is not equal", "bold")
        self.assertNotEqual(node.text, node2.text)
    
    def test_text_type_not_eq(self):
        node = TextNode("This is some text", "underline", "https://boot.dev")
        node2 = TextNode("This is also some text", "bold", None)
        self.assertNotEqual(node.text_type, node2.text_type)
    
        
    def test_url__not_eq(self):
        node = TextNode("This is some text", "bold", "https://boot.dev")
        node2 = TextNode("This is also some text", "italics", None)
        self.assertNotEqual(node.url, node2.url)
        
        
if __name__ == "__main__":
    unittest.main()