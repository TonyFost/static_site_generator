import unittest

from textnode import TextNode
from markdown_parse import split_nodes_delimiter
from markdown_parse import extract_markdown_images
from markdown_parse import extract_markdown_links
from markdown_parse import split_nodes_image
from markdown_parse import split_nodes_link
from markdown_parse import text_to_textnodes
from markdown_parse import markdown_to_blocks
from markdown_parse import block_to_block_type
from markdown_parse import handle_quote
from markdown_parse import handle_list
from markdown_parse import handle_code
from markdown_parse import handle_header
from markdown_parse import handle_paragraph
from markdown_parse import markdown_to_html_node


class TestTextNode(unittest.TestCase):
    def test_markdown_parse_to_delimiter_uneven(self):
        node = TextNode("bad *text", "text")
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(cm.exception.args[0], "Uneven delimiter * in node text: bad *text")

    def test_markdown_parse_to_delimiter_not_list(self):
        node = TextNode("bad *text", "text")
        with self.assertRaises(TypeError) as cm:
            split_nodes_delimiter(node, "*", "italic")
        self.assertEqual(cm.exception.args[0], "Expected list of TextNodes, received TextNode")

    def test_markdown_parse_to_delimiter_italic(self):
        node = TextNode("good italic *text* is good", "text")
        node_list = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(node_list[0].text, "good italic ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "italic")
        self.assertEqual(node_list[2].text, " is good")
        self.assertEqual(node_list[2].text_type, "text")

    def test_markdown_parse_to_delimiter_bold(self):
        node = TextNode("good bold **text** is good", "text")
        node_list = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(node_list[0].text, "good bold ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "bold")
        self.assertEqual(node_list[2].text, " is good")
        self.assertEqual(node_list[2].text_type, "text")

    def test_markdown_parse_to_delimiter_code(self):
        node = TextNode("good code `text` is good", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "good code ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "code")
        self.assertEqual(node_list[2].text, " is good")
        self.assertEqual(node_list[2].text_type, "text")

    def test_markdown_parse_to_delimiter_at_end(self):
        node = TextNode("good code `text`", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "good code ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "text")
        self.assertEqual(node_list[1].text_type, "code")

    def test_markdown_parse_to_delimiter_at_start(self):
        node = TextNode("`text` code", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "text")
        self.assertEqual(node_list[0].text_type, "code")
        self.assertEqual(node_list[1].text, " code")
        self.assertEqual(node_list[1].text_type, "text")

    def test_markdown_parse_to_delimiter_only_delimiter(self):
        node = TextNode("`text`", "text")
        node_list = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(node_list[0].text, "text")
        self.assertEqual(node_list[0].text_type, "code")

    def test_markdown_parse_markdown_images_only(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(extracted_images[0][0], "rick roll")
        self.assertEqual(extracted_images[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(extracted_images[1][0], "obi wan")
        self.assertEqual(extracted_images[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_markdown_parse_markdown_links_only(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links[0][0], "to boot dev")
        self.assertEqual(extracted_links[0][1], "https://www.boot.dev")
        self.assertEqual(extracted_links[1][0], "to youtube")
        self.assertEqual(extracted_links[1][1], "https://www.youtube.com/@bootdotdev")

    def test_markdown_parse_markdown_images_before(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(extracted_images[0][0], "rick roll")
        self.assertEqual(extracted_images[0][1], "https://i.imgur.com/aKaOqIh.gif")

    def test_markdown_parse_markdown_link_before(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links[0][0], "to boot dev")
        self.assertEqual(extracted_links[0][1], "https://www.boot.dev")

    def test_markdown_parse_markdown_images_after(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(extracted_images[0][0], "obi wan")
        self.assertEqual(extracted_images[0][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_markdown_parse_markdown_link_after(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links[0][0], "to youtube")
        self.assertEqual(extracted_links[0][1], "https://www.youtube.com/@bootdotdev")

    def test_markdown_parse_image_delimiter_not_list(self):
        node = TextNode("bad *text", "text")
        with self.assertRaises(TypeError) as cm:
            split_nodes_image(node)
        self.assertEqual(cm.exception.args[0], "Expected list of TextNodes, received TextNode")

    def test_markdown_parse_image_delimiter_only_images(self):
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

    def test_markdown_parse_link_delimiter_not_list(self):
        node = TextNode("bad *text", "text")
        with self.assertRaises(TypeError) as cm:
            split_nodes_link(node)
        self.assertEqual(cm.exception.args[0], "Expected list of TextNodes, received TextNode")

    def test_markdown_parse_link_delimiter_only_links(self):
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

    def test_markdown_parse_image_delimiter_images_before(self):
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

    def test_markdown_parse_link_delimiter_link_before(self):
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

    def test_markdown_parse_image_delimiter_images_after(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node = TextNode(text, "text")
        node_list = split_nodes_image([node])
        self.assertEqual(node_list[0].text, "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "obi wan")
        self.assertEqual(node_list[1].text_type, "image")
        self.assertEqual(node_list[1].url, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_markdown_parse_link_delimiter_link_after(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, "text")
        node_list = split_nodes_link([node])
        self.assertEqual(node_list[0].text, "This is text with a link ![to boot dev](https://www.boot.dev) and ")
        self.assertEqual(node_list[0].text_type, "text")
        self.assertEqual(node_list[1].text, "to youtube")
        self.assertEqual(node_list[1].text_type, "link")
        self.assertEqual(node_list[1].url, "https://www.youtube.com/@bootdotdev")

    def test_markdown_parse_link_delimiter_link_surrounded_by_images(self):
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

    def test_markdown_parse_link_delimiter_link_surrounds_image(self):
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

    def test_markdown_parse_text_to_textnodes(self):
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

    def test_markdown_parse_markdown_to_blocks_easy_sample(self):
        markdown ="""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        check = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                 ]
        blocks = markdown_to_blocks(markdown)
        for i in range(len(check)):
            self.assertEqual(check[i], blocks[i])

    def test_markdown_parse_markdown_to_blocks_extra_new_lines(self):
        markdown ="""# This is a heading

        
This is a paragraph of text. It has some **bold** and *italic* words inside of it.



* This is the first list item in a list block
* This is a list item
* This is another list item

This is text without any markdown.
Some more text without any markdown.
Next some extra lines at the end
                    
                    
                    
"""
        check = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            "This is text without any markdown.\nSome more text without any markdown.\nNext some extra lines at the end"
                 ]
        blocks = markdown_to_blocks(markdown)
        for i in range(len(check)):
            self.assertEqual(check[i], blocks[i])

    def test_markdown_parse_block_to_block_type_paragraph(self):
        block = "This is a block without markdown."
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_heading(self):
        block = "# This is a basic header"
        result = block_to_block_type(block)
        self.assertEqual(result, "heading")

    def test_markdown_parse_block_to_block_type_heading_levels_good(self):
        block2 = "## This is a basic header"
        block3 = "### This is a basic header"
        block4 = "#### This is a basic header"
        block5 = "##### This is a basic header"
        block6 = "###### This is a basic header"
        result = block_to_block_type(block2)
        self.assertEqual(result, "heading")
        result = block_to_block_type(block3)
        self.assertEqual(result, "heading")
        result = block_to_block_type(block4)
        self.assertEqual(result, "heading")
        result = block_to_block_type(block5)
        self.assertEqual(result, "heading")
        result = block_to_block_type(block6)
        self.assertEqual(result, "heading")

    def test_markdown_parse_block_to_block_type_heading_level_bad(self):
        block = "####### This is a basic header"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_heading_no_space(self):
        block = "####This is a basic header"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_heading_other_whitespace(self):
        block = "####\tThis is a basic header"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_heading_newline_bad(self):
        block = "####\n This is a basic header"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_code(self):
        block = "```This is a basic code block```"
        result = block_to_block_type(block)
        self.assertEqual(result, "code")

    def test_markdown_parse_block_to_block_type_code_only_backtick(self):
        block = "``````"
        result = block_to_block_type(block)
        self.assertEqual(result, "code")

    def test_markdown_parse_block_to_block_type_code_not_closed(self):
        block = "```This is a basic code block"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_code_only_backtick_not_6(self):
        block = "`````"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_quote(self):
        block = ">This is a basic quoteblock"
        result = block_to_block_type(block)
        self.assertEqual(result, "quote")

    def test_markdown_parse_block_to_block_type_quote_multi_line(self):
        block = """>This is a basic quoteblock
>This is more of a quote block
>Continuing quote block
>Another line
>Last line of quote block"""
        result = block_to_block_type(block)
        self.assertEqual(result, "quote")

    def test_markdown_parse_block_to_block_type_quote_missed_one_line(self):
        block = """>This is a basic quoteblock
>This is more of a quote block
>Continuing quote block
## Ooops, dropped a line trying to add a header
>Last line of quote block"""
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_unordered_list_asterisk(self):
        block = "* This is a basic unordered_list"
        result = block_to_block_type(block)
        self.assertEqual(result, "unordered_list")

    def test_markdown_parse_block_to_block_type_unordered_list_asterisk_multiline(self):
        block = """* This is a basic unordered_list
* next item
* additional item
* another item
* last item"""
        result = block_to_block_type(block)
        self.assertEqual(result, "unordered_list")

    def test_markdown_parse_block_to_block_type_unordered_list_dash(self):
        block = "- This is a another basic unordered_list"
        result = block_to_block_type(block)
        self.assertEqual(result, "unordered_list")

    def test_markdown_parse_block_to_block_type_unordered_list_dash_multiline(self):
        block = """- This is a basic unordered_list
- next item
- additional item
- another item
- last item"""
        result = block_to_block_type(block)
        self.assertEqual(result, "unordered_list")

    def test_markdown_parse_block_to_block_type_unordered_list_asterisk_bad_space(self):
        block = """* This is a bad unordered_list
*next item
* additional item
* another item
* last item"""
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_unordered_list_asterisk_missing(self):
        block = """* This is a bad unordered_list
* next item
* additional item
 another item
* last item"""
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_ordered_list(self):
        block = "1. This is a basic ordered list."
        result = block_to_block_type(block)
        self.assertEqual(result, "ordered_list")

    def test_markdown_parse_block_to_block_type_ordered_list_multiline(self):
        block = """1. This is a basic ordered list.
2. This is another item
3. This is a third item
4. This is a fourth item
5. This is a fifth item
6. item
7. sorry I stopped counting
8. this is something
9. might be something
10. last item
11. just kidding here's the last one"""
        result = block_to_block_type(block)
        self.assertEqual(result, "ordered_list")

    def test_markdown_parse_block_to_block_type_ordered_list_multiline_missing_number(self):
        block = """1. This is a basic ordered list.
2. This is another item
3. This is a third item
4. This is a fourth item
5. This is a fifth item
6. item
7. sorry I stopped counting
9. might be something
10. last item
11. just kidding here's the last one"""
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_ordered_list_not_starting_at_one(self):
        block = """0. Zero index ftl
1. This is a basic ordered list.
2. This is another item
3. This is a third item
4. This is a fourth item
5. This is a fifth item
6. item
7. sorry I stopped counting
8. this is something
9. might be something
10. last item
11. just kidding here's the last one"""
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_ordered_list_multiline_missing_space(self):
        block = """1. This is a basic ordered list.
2. This is another item
3. This is a third item
4. This is a fourth item
5. This is a fifth item
6. item
7. sorry I stopped counting
8.This item is missing a space
9. might be something
10. last item
11. just kidding here's the last one"""
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_block_to_block_type_ordered_list_multiline_missing_item(self):
        block = """1. This is a basic ordered list.
2. This is another item
3. This is a third item
4. This is a fourth item
5. This is a fifth item
6. item
7. sorry I stopped counting
8.
9. might be something
10. last item
11. just kidding here's the last one"""
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_markdown_parse_handle_quote(self):
        block = """>This is a basic quoteblock
>This is more of a quote block
>Continuing quote block
>Another line
>Last line of quote block"""
        result = handle_quote(block)
        self.assertEqual(result.tag, "quoteblock")

    def test_markdown_parse_handle_list_unordered_dash(self):
        block = """- This is a basic unordered_list
- next item
- additional item
- another item
- last item"""
        result = handle_list(block)
        self.assertEqual(result.tag, None)
        items = result.children
        for item in items:
            self.assertEqual(item.tag, "li")

    def test_markdown_parse_handle_list_unordered_asterisk(self):
        block = """* This is a basic unordered_list
* next item
* additional item
* another item
* last item"""
        result = handle_list(block)
        self.assertEqual(result.tag, None)
        items = result.children
        for item in items:
            self.assertEqual(item.tag, "li")

    def test_markdown_parse_handle_list_ordered(self):
        block = """1. This is a basic ordered list.
2. This is another item
3. This is a third item
4. This is a fourth item
5. This is a fifth item
6. item
7. sorry I stopped counting
8. 
9. might be something
10. last item
11. just kidding here's the last one"""
        result = handle_list(block)
        self.assertEqual(result.tag, None)
        items = result.children
        for item in items:
            self.assertEqual(item.tag, "li")

    def test_markdown_parse_handle_header(self):
        block1 = "# This is a basic header"
        block2 = "## This is a basic header"
        block3 = "### This is a basic header"
        block4 = "#### This is a basic header"
        block5 = "##### This is a basic header"
        block6 = "###### This is a basic header"
        result = handle_header(block1)
        self.assertEqual(result.tag, "h1")
        result = handle_header(block2)
        self.assertEqual(result.tag, "h2")
        result = handle_header(block3)
        self.assertEqual(result.tag, "h3")
        result = handle_header(block4)
        self.assertEqual(result.tag, "h4")
        result = handle_header(block5)
        self.assertEqual(result.tag, "h5")
        result = handle_header(block6)
        self.assertEqual(result.tag, "h6")

    def test_markdown_parse_handle_paragraph(self):
        block = """>This is a basic quoteblock
>This is more of a quote block
>Continuing quote block
## Ooops, dropped a line trying to add a header
>Last line of quote block"""
        result = handle_paragraph(block)
        self.assertEqual(result.tag, "p")

    def test_markdown_parse_handle_paragraph(self):
        block = """```>This is a basic quoteblock
>This is more of a quote block
>Continuing quote block
## **Ooops**, dropped a line trying to add a header
>Last line of quote block```"""
        result = handle_code(block)
        self.assertEqual(result.tag, "pre")
        result = result.children[0]
        self.assertEqual(result.tag, "code")

    def test_markdown_parse_markdown_to_html_node(self):
        block = """This is a paragraph.

>This is a basic quoteblock
>This is more of a quote block

1. item 1
2. item 2
3. item 3

### Heading level 3

```Some code block
conitnued```

- item a
- item b
- item c

"""
        result = markdown_to_html_node(block)
        self.assertEqual(result.tag, "div")
        node_types = ['p', 'quoteblock', 'ol', 'h3', 'pre', 'ul']
        for i, type in enumerate(node_types):
            self.assertEqual(result.children[i].tag, type)

    #def test_markdown_parse_(self):

if __name__ == "__main__":
    unittest.main()
