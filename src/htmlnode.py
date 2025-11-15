class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children if children else []
        self.props = props if props else {}
    
    #def __str__(self):
    #    attrs = " ".join(f'{key}="{value}"' for key, value in self.props.items())
    #    if attrs:
    #        return f"<{self.tag} {attrs}>{self.value}</{self.tag}>"
    #    return f"<{self.tag}>{self.value}</{self.tag}>"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
    
    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props}, children={self.children})"

class HTMLTags:
    DIV = "div"
    SPAN = "span"
    P = "p"
    A = "a"
    IMG = "img"
    UL = "ul"
    LI = "li"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    