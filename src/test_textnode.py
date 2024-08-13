import unittest

from textnode import TextNode
from leafnode import LeafNode
from textnode import text_node_to_html_node
from textnode import split_nodes_delimiter


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

    def test_text_node_to_delimiter_uneven(self):
        node = TextNode("bad *text", "text")
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(cm.exception.args[0], "Uneven delimiter * in node text: bad *text")

    def test_text_node_to_delimiter_not_list(self):
        node = TextNode("bad *text", "text")
        with self.assertRaises(TypeError) as cm:
            split_nodes_delimiter(node, "*", "italic")
        self.assertEqual(cm.exception.args[0], "Expected list of TextNodes, received TextNode")

    def test_text_node_to_delimiter_italic(self):
        node = TextNode("good italic *text* is good", "text")
        node_list = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(node_list[0].text, "good italic ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "italic")
        self.assertEqual(node_list[2].text, " is good")
        self.assertEqual(node_list[2].text_type, "text")

    def test_text_node_to_delimiter_bold(self):
        node = TextNode("good bold **text** is good", "text")
        node_list = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(node_list[0].text, "good bold ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "bold")
        self.assertEqual(node_list[2].text, " is good")
        self.assertEqual(node_list[2].text_type, "text")

    def test_text_node_to_delimiter_code(self):
        node = TextNode("good code `text` is good", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "good code ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "code")
        self.assertEqual(node_list[2].text, " is good")
        self.assertEqual(node_list[2].text_type, "text")

    def test_text_node_to_delimiter_at_end(self):
        node = TextNode("good code `text`", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "good code ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "code")
        self.assertEqual(node_list[2].text, "")
        self.assertEqual(node_list[2].text_type, "text")

    def test_text_node_to_delimiter_at_start(self):
        node = TextNode("`text` code", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "code")
        self.assertEqual(node_list[2].text, " code")
        self.assertEqual(node_list[2].text_type, "text")

    def test_text_node_to_delimiter_only_delimiter(self):
        node = TextNode("`text`", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "code")
        self.assertEqual(node_list[2].text, "")
        self.assertEqual(node_list[2].text_type, "text")

    # def test_text_node_(self):
    #     node = TextNode("text", "text_type")
    #     self.assertEqual(node.__repr__(), "TextNode(text, text_type)")



if __name__ == "__main__":
    unittest.main()
