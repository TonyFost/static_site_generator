import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "http://localhost:8888")
        self.assertNotEqual(node, node2)

    def test_print(self):
        node = TextNode("text", "text_type", "url")
        self.assertEqual(node.__repr__(), "TextNode(text, text_type, url)")

    def test_print_no_url(self):
        node = TextNode("text", "text_type")
        self.assertEqual(node.__repr__(), "TextNode(text, text_type)")



if __name__ == "__main__":
    unittest.main()
