from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        if value is None:
            raise ValueError("LeafNode must have a value.")
        
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return f"{self.value}"
        html_props = super().props_to_html()
        return f'<{self.tag}{html_props}>{self.value}</{self.tag}>'
        
    def __repr__(self):
        return (f"LeafNode(\n"
                f"  tag={self.tag!r},\n"
                f"  value={self.value!r},\n"
                f"  props={self.props!r}\n"
                f")")