from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("No value passed to Lead Node")

        if self.tag:
            open_tag = f"<{self.tag}{self.props_to_html()}>"
            close_tag = f"</{self.tag}>"
            return open_tag + self.value + close_tag
        else:
            return self.value

