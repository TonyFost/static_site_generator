import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_NotImplementedError(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_values(self):
        node = HTMLNode("tag", "value", [], {})
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})



if __name__ == "__main__":
    unittest.main()