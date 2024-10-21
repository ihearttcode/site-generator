

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("HTML nodes must have a valid tag!")
        
        # If the node has children, recursively convert them to HTML
        child_html = ''.join([child.to_html() for child in self.children]) if self.children else ''
        
        # If it's a self-closing tag (e.g., img), handle accordingly
        if self.tag in ['img', 'br', 'hr', 'meta']:
            return f'<{self.tag}{self.props_to_html()} />'
        
        # For regular nodes with opening and closing tags
        return f'<{self.tag}{self.props_to_html()}>{child_html or self.value}</{self.tag}>'
    
    def props_to_html(self):
        if self.props is None:
            return ''
        html_str = ''
        for prop, value in self.props.items():
            html_str += f' {prop}="{value}"'
        return html_str
    
    def __repr__(self) -> str:
        return (f"HTMLNode(\n"
                f"  tag={self.tag!r},\n"
                f"  value={self.value!r},\n"
                f"  children={self.children!r},\n"
                f"  props={self.props!r}\n"
                f")")