import unittest

from textnode import TextNode
from leafnode import LeafNode
from textnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_text_node_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_node_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "http://localhost:8888")
        self.assertNotEqual(node, node2)

    def test_text_node_print(self):
        node = TextNode("text", "text_type", "url")
        self.assertEqual(node.__repr__(), "TextNode(text, text_type, url)")

    def test_text_node_print_no_url(self):
        node = TextNode("text", "text_type")
        self.assertEqual(node.__repr__(), "TextNode(text, text_type)")

    def test_text_node_node_is_leaf_node(self):
        node = TextNode("Some text", "text")
        l_node = text_node_to_html_node(node)
        self.assertIsInstance(l_node, LeafNode)

    def test_text_node_to_leaf_node_text(self):
        node = TextNode("Some text", "text")
        l_node = text_node_to_html_node(node)
        self.assertEqual(l_node.tag, None)
        self.assertEqual(l_node.value, "Some text")

    def test_text_node_to_leaf_node_bold(self):
        node = TextNode("Some text", "bold")
        l_node = text_node_to_html_node(node)
        self.assertEqual(l_node.tag, "b")
        self.assertEqual(l_node.value, "Some text")

    def test_text_node_to_leaf_node_italic(self):
        node = TextNode("Some text", "italic")
        l_node = text_node_to_html_node(node)
        self.assertEqual(l_node.tag, "i")
        self.assertEqual(l_node.value, "Some text")

    def test_text_node_to_leaf_node_code(self):
        node = TextNode("Some text", "code")
        l_node = text_node_to_html_node(node)
        self.assertEqual(l_node.tag, "code")
        self.assertEqual(l_node.value, "Some text")

    def test_text_node_to_leaf_node_link(self):
        node = TextNode("Some text", "link", "URL")
        l_node = text_node_to_html_node(node)
        self.assertEqual(l_node.tag, "a")
        self.assertEqual(l_node.value, "Some text")
        self.assertEqual(l_node.props, {"href": "URL"})

    def test_text_node_to_leaf_node_img(self):
        node = TextNode("alt text", "image", "URL")
        l_node = text_node_to_html_node(node)
        self.assertEqual(l_node.tag, "img")
        self.assertEqual(l_node.value, "")
        self.assertEqual(l_node.props, {"src": "URL", "alt": "alt text"})

    def test_text_node_to_leaf_node_invalid(self):
        node = TextNode("alt text", "invalid", "URL")
        with self.assertRaises(Exception) as cm:
            text_node_to_html_node(node)
        self.assertEqual(cm.exception.args[0], "Unknown TextNode text type")

    # def test_text_node_(self):
    #     node = TextNode("text", "text_type")
    #     self.assertEqual(node.__repr__(), "TextNode(text, text_type)")



if __name__ == "__main__":
    unittest.main()
