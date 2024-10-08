from leafnode import LeafNode

class TextNode():
    def __init__(self, text:str, text_type:str, url:str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        return self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})" if self.url else f"TextNode({self.text}, {self.text_type})"


def text_node_to_html_node(text_node:TextNode):
    match(text_node.text_type):
        case("text"):
            return LeafNode(None, text_node.text)
        case("bold"):
            return LeafNode("b", text_node.text)
        case("italic"):
            return LeafNode("i", text_node.text)
        case("code"):
            return LeafNode("code", text_node.text)
        case("link"):
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case("image"):
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown TextNode text type")

def main():
    new_text_node = TextNode("This is a text node", "bold", "https://github.com/TonyFost")
    print(new_text_node)

if __name__ == "__main__":
    main()