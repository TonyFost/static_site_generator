
class TextNode():
    def __init__(self, text:str, text_type:str, url:str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        return self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})" if self.url else f"TextNode({self.text}, {self.text_type})"



def main():
    new_text_node = TextNode("This is a text node", "bold", "https://github.com/TonyFost")
    print(new_text_node)

if __name__ == "__main__":
    main()