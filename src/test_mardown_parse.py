import unittest

from textnode import TextNode
from markdown_parse import split_nodes_delimiter
from markdown_parse import extract_markdown_images
from markdown_parse import extract_markdown_links
from markdown_parse import split_nodes_image
from markdown_parse import split_nodes_link
from markdown_parse import text_to_textnodes


class TestTextNode(unittest.TestCase):
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

    def test_text_node_to_delimiter_at_start(self):
        node = TextNode("`text` code", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "text")
        self.assertEqual(node_list[0].text_type, "code")
        self.assertEqual(node_list[1].text, " code")
        self.assertEqual(node_list[1].text_type, "text")

    def test_text_node_to_delimiter_only_delimiter(self):
        node = TextNode("`text`", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "text")
        self.assertEqual(node_list[0].text_type, "code")

    def test_text_node_markdown_images_only(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(extracted_images[0][0], "rick roll")
        self.assertEqual(extracted_images[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(extracted_images[1][0], "obi wan")
        self.assertEqual(extracted_images[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_text_node_markdown_links_only(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links[0][0], "to boot dev")
        self.assertEqual(extracted_links[0][1], "https://www.boot.dev")
        self.assertEqual(extracted_links[1][0], "to youtube")
        self.assertEqual(extracted_links[1][1], "https://www.youtube.com/@bootdotdev")

    def test_text_node_markdown_images_before(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(extracted_images[0][0], "rick roll")
        self.assertEqual(extracted_images[0][1], "https://i.imgur.com/aKaOqIh.gif")

    def test_text_node_markdown_link_before(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links[0][0], "to boot dev")
        self.assertEqual(extracted_links[0][1], "https://www.boot.dev")

    def test_text_node_markdown_images_after(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(extracted_images[0][0], "obi wan")
        self.assertEqual(extracted_images[0][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_text_node_markdown_link_after(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links[0][0], "to youtube")
        self.assertEqual(extracted_links[0][1], "https://www.youtube.com/@bootdotdev")

    def test_text_node_image_delimiter_not_list(self):
        node = TextNode("bad *text", "text")
        with self.assertRaises(TypeError) as cm:
            split_nodes_image(node)
        self.assertEqual(cm.exception.args[0], "Expected list of TextNodes, received TextNode")

    def test_text_node_image_delimiter_only_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node = TextNode(text, "text")
        node_list = split_nodes_image([node])
        self.assertEqual(node_list[0].text, "This is text with a ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "rick roll")
        self.assertEqual(node_list[1].text_type, "image")
        self.assertEqual(node_list[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(node_list[2].text, " and ")
        self.assertEqual(node_list[2].text_type, "text")
        self.assertEqual(node_list[3].text, "obi wan")
        self.assertEqual(node_list[3].text_type, "image")
        self.assertEqual(node_list[3].url, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_text_node_link_delimiter_not_list(self):
        node = TextNode("bad *text", "text")
        with self.assertRaises(TypeError) as cm:
            split_nodes_link(node)
        self.assertEqual(cm.exception.args[0], "Expected list of TextNodes, received TextNode")

    def test_text_node_link_delimiter_only_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, "text")
        node_list = split_nodes_link([node])
        self.assertEqual(node_list[0].text, "This is text with a link ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "to boot dev")
        self.assertEqual(node_list[1].text_type, "link")
        self.assertEqual(node_list[1].url, "https://www.boot.dev")
        self.assertEqual(node_list[2].text, " and ")
        self.assertEqual(node_list[2].text_type, "text")
        self.assertEqual(node_list[3].text, "to youtube")
        self.assertEqual(node_list[3].text_type, "link")
        self.assertEqual(node_list[3].url, "https://www.youtube.com/@bootdotdev")

    def test_text_node_image_delimiter_images_before(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node = TextNode(text, "text")
        node_list = split_nodes_image([node])
        self.assertEqual(node_list[0].text, "This is text with a ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "rick roll")
        self.assertEqual(node_list[1].text_type, "image")
        self.assertEqual(node_list[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(node_list[2].text, " and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(node_list[2].text_type, "text")

    def test_text_node_link_delimiter_link_before(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, "text")
        node_list = split_nodes_link([node])
        self.assertEqual(node_list[0].text, "This is text with a link ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "to boot dev")
        self.assertEqual(node_list[1].text_type, "link")
        self.assertEqual(node_list[1].url, "https://www.boot.dev")
        self.assertEqual(node_list[2].text, " and ![to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(node_list[2].text_type, "text")

    def test_text_node_image_delimiter_images_after(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node = TextNode(text, "text")
        node_list = split_nodes_image([node])
        self.assertEqual(node_list[0].text, "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "obi wan")
        self.assertEqual(node_list[1].text_type, "image")
        self.assertEqual(node_list[1].url, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_text_node_link_delimiter_link_after(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, "text")
        node_list = split_nodes_link([node])
        self.assertEqual(node_list[0].text, "This is text with a link ![to boot dev](https://www.boot.dev) and ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "to youtube")
        self.assertEqual(node_list[1].text_type, "link")
        self.assertEqual(node_list[1].url, "https://www.youtube.com/@bootdotdev")

    def test_text_node_link_delimiter_link_surrounded_by_images(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev), and then another image ![to boot dev](https://www.boot.dev)"
        node = TextNode(text, "text")
        node_list = split_nodes_link([node])
        self.assertEqual(node_list[0].text, "This is text with a link ![to boot dev](https://www.boot.dev) and ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "to youtube")
        self.assertEqual(node_list[1].text_type, "link")
        self.assertEqual(node_list[1].url, "https://www.youtube.com/@bootdotdev")
        self.assertEqual(node_list[2].text, ", and then another image ![to boot dev](https://www.boot.dev)")
        self.assertEqual(node_list[2].text_type, "text")

    def test_text_node_link_delimiter_link_surrounds_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) with another link here [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, "text")
        node_list = split_nodes_link([node])
        self.assertEqual(node_list[0].text, "This is text with a link ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "to boot dev")
        self.assertEqual(node_list[1].text_type, "link")
        self.assertEqual(node_list[1].url, "https://www.boot.dev")
        self.assertEqual(node_list[2].text, " and ![to youtube](https://www.youtube.com/@bootdotdev) with another link here ")
        self.assertEqual(node_list[2].text_type, "text")
        self.assertEqual(node_list[3].text, "to youtube")
        self.assertEqual(node_list[3].text_type, "link")
        self.assertEqual(node_list[3].url, "https://www.youtube.com/@bootdotdev")

    def test_text_node_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_list = text_to_textnodes(text)
        check_node_list = [
                            TextNode("This is ", "text"),
                            TextNode("text", "bold"),
                            TextNode(" with an ", "text"),
                            TextNode("italic", "italic"),
                            TextNode(" word and a ", "text"),
                            TextNode("code block", "code"),
                            TextNode(" and an ", "text"),
                            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", "text"),
                            TextNode("link", "link", "https://boot.dev"),
                        ]
        self.assertEqual(node_list, check_node_list)


if __name__ == "__main__":
    unittest.main()
