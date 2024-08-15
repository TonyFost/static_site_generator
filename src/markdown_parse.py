from textnode import TextNode
import re
from htmlnode import HTMLNode

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

            while delimited_texts[0][-1] == "!": #check if it was an image
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
    base_text_node = TextNode(text, "text")
    text_node_list = split_nodes_delimiter([base_text_node], "**", "bold")
    text_node_list = split_nodes_delimiter(text_node_list, "*", "italic")
    text_node_list = split_nodes_delimiter(text_node_list, "`", "code")
    text_node_list = split_nodes_image(text_node_list)
    text_node_list = split_nodes_link(text_node_list)
    return text_node_list
