import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_empty(self):
        node = ParentNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        node = ParentNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_to_html_ValueError(self):
        node = ParentNode("b")
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_ValueError(self):
        l_node = LeafNode("p", "This is a paragraph")
        node = ParentNode(children=[l_node])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_tag_children(self):
        l_node = LeafNode("b", "This is a paragraph")
        node = ParentNode("p", children=[l_node])
        self.assertEqual(node.to_html(), "<p><b>This is a paragraph</b></p>")

    def test_to_html_tag_children_props(self):
        l_node1 = LeafNode(value="Some text. ")
        l_node2 = LeafNode("a", "This is a link", {"href": "https://www.google.com", "target": "_blank"})
        l_node3 = LeafNode(value=" with some other text after.")
        node = ParentNode("p", children=[l_node1, l_node2, l_node3])
        self.assertEqual(node.to_html(), "<p>Some text. <a href=\"https://www.google.com\" target=\"_blank\">This is a link</a> with some other text after.</p>")

    def test_values(self):
        node = ParentNode("tag", ["children"], {})
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, ["children"])
        self.assertEqual(node.props, {})



if __name__ == "__main__":
    unittest.main()