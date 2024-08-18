from textnode import TextNode
from textnode import text_node_to_html_node
from parentnode import ParentNode
import re

def split_nodes_delimiter(old_nodes:list, delimiter, text_type):
    new_nodes_list = []

    if type(old_nodes) != list:
        raise TypeError(f"Expected list of TextNodes, received {type(old_nodes).__name__}")

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes_list.append(node)
            continue

        delimited_texts = node.text.split(delimiter)
        if len(delimited_texts) == 1:
            new_nodes_list.append(node)
            continue

        if len(delimited_texts) % 2 == 0:
            raise ValueError(f"Uneven delimiter {delimiter} in node text: {node.text}")
        
        for i in range(len(delimited_texts)):
            node_text = delimited_texts[i]
            node_text_type = "text" if i % 2 == 0 else text_type
            if node_text:
                new_nodes_list.append(TextNode(node_text, node_text_type))

    return new_nodes_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    # matches = re.findall(r"(?:[^!])[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes_list = []

    if type(old_nodes) != list:
        raise TypeError(f"Expected list of TextNodes, received {type(old_nodes).__name__}")

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes_list.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes_list.append(node)
            continue
            
        current_text = node.text
        for image in images:
            delimiter = f"![{image[0]}]({image[1]})"
            delimited_texts = current_text.split(delimiter, 1)

            new_nodes_list.append(TextNode(delimited_texts[0], "text"))
            new_nodes_list.append(TextNode(image[0], "image", image[1]))
            current_text = delimited_texts[1]

        if current_text:
            new_nodes_list.append(TextNode(current_text, "text"))

    return new_nodes_list

def split_nodes_link(old_nodes):
    new_nodes_list = []

    if type(old_nodes) != list:
        raise TypeError(f"Expected list of TextNodes, received {type(old_nodes).__name__}")

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes_list.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes_list.append(node)
            continue

        skip_delimiter_text = ""
        current_text = node.text
        for link in links:
            delimiter = f"[{link[0]}]({link[1]})"
            delimited_texts = current_text.split(delimiter, 1)

            while delimited_texts[0] and delimited_texts[0][-1] == "!": #check if it was an image

                skip_delimiter_text += delimited_texts[0] + delimiter
                current_text = delimited_texts[1]
                delimited_texts = current_text.split(delimiter, 1)

            new_nodes_list.append(TextNode(skip_delimiter_text + delimited_texts[0], "text"))
            new_nodes_list.append(TextNode(link[0], "link", link[1]))
            current_text = delimited_texts[1]
            skip_delimiter_text = ""

        if current_text:
            new_nodes_list.append(TextNode(current_text, "text"))

    return new_nodes_list

def text_to_textnodes(text):
    base_text_node = [TextNode(text, "text")]
    text_node_list = split_nodes_delimiter(base_text_node, "**", "bold")
    text_node_list = split_nodes_delimiter(text_node_list, "*", "italic")
    text_node_list = split_nodes_delimiter(text_node_list, "`", "code")
    text_node_list = split_nodes_image(text_node_list)
    text_node_list = split_nodes_link(text_node_list)
    return text_node_list


def markdown_to_blocks(markdown):
    blocks = [line.strip() for line in markdown.split("\n\n") if line != ""]
    return blocks

def block_to_block_type(md_block):
    # check header block
    max_header_length = 6
    for i in range(len(md_block)):
        if i > max_header_length:
            break

        c = md_block[i]
        if c == "#":
            continue
        elif i > 0 and c == " ":
            return "heading"
        else:
            break
    
    # check code block
    if len(md_block) >= 6:
        check = md_block[:3]
        if check == "```" and check == md_block[-3:]:
            return "code"
        
    #checks after here need to check every line
    lines = md_block.split("\n")
    
    #check for quoteblock
    check = False
    for line in lines:
        if line[0] == ">":
            check = True
        else:
            check = False
            break
    if check:
        return "quote"

    #check for unordered list
    check = False
    for line in lines:
        if len(line) < 2:
            check = False
            break

        if line[:2] == "* " or line[:2] == "- ":
            check = True
        else:
            check = False
            break
    if check:
        return "unordered_list"

    #check for ordered list
    check = False
    for i in range(len(lines)):
        line = lines[i]
        length_of_check = len(str(i+1)) + 2
        if len(line) < length_of_check:
            check = False
            break

        if line[:length_of_check] == f"{i+1}. ":
            check = True
        else:
            check = False
            break
    if check:
        return "ordered_list"
    
    return "paragraph"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match (block_type):
            case ('quote'):
                html_node = handle_quote(block)
            case('unordered_list'):
                html_node = handle_list(block)
                html_node.tag = 'ul'
            case('ordered_list'):
                html_node = handle_list(block)
                html_node.tag = 'ol'
            case ('code'):
                html_node = handle_code(block)
            case ('heading'):
                html_node = handle_header(block)
            case ('paragraph'):
                html_node = handle_paragraph(block)
        
        nodes.append(html_node)

    return ParentNode('div', nodes) 

def help_transform_textnode_to_leafnode(text_nodes):
    for i in range(len(text_nodes)):
        text_nodes[i] = text_node_to_html_node(text_nodes[i])
    return text_nodes

def handle_quote(block):
    text = block.lstrip('> ').lstrip('>').replace('\n> ', '\n').replace('\n>', '\n')
    children = text_to_textnodes(text)
    help_transform_textnode_to_leafnode(children)
    return ParentNode('blockquote', children)

def handle_list(block):
    items = block.split('\n')
    list_children = []
    for item in items:
        text_nodes = text_to_textnodes(item.split(' ', 1)[1])
        help_transform_textnode_to_leafnode(text_nodes)
        list_children.append(ParentNode('li', text_nodes))

    return ParentNode(children=list_children)

def handle_code(block):
    children = text_to_textnodes(block[3:-3])
    help_transform_textnode_to_leafnode(children)
    code_node = ParentNode('code', children)
    return ParentNode('pre', [code_node])

def handle_header(block):
    text = block.split(' ', 1)
    header_count = len(text[0])
    children = text_to_textnodes(text[1])
    help_transform_textnode_to_leafnode(children)
    return ParentNode(f"h{header_count}", children)

def handle_paragraph(block):
    children = text_to_textnodes(block)
    help_transform_textnode_to_leafnode(children)
    return ParentNode('p', children)


def extract_title(markdown):
    md_lines = markdown.split('\n')
    for line in md_lines:
        if len(line) >= 3 and line[:2] == "# ":
            return line[2:]
        
    raise Exception("Unable to determine title, no h1 header")
