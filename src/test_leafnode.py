import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_empty(self):
        node = LeafNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_leaf_node_props_to_html(self):
        node = LeafNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_leaf_node_to_html_ValueError(self):
        node = LeafNode("b")
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_node_to_html_tag_value(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_leaf_node_to_html_tag_value_props(self):
        node = LeafNode("a", "This is a link", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">This is a link</a>")

    def test_leaf_node_to_html_value(self):
        node = LeafNode(value="This is a paragraph")
        self.assertEqual(node.to_html(), "This is a paragraph")

    def test_leaf_node_values(self):
        node = LeafNode("tag", "value", {})
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {})



if __name__ == "__main__":
    unittest.main()