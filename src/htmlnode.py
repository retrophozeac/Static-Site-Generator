class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value =value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        st = ""
        for key, value in self.props.items():
            st1 = " "+key +"=\""+value +"\""
            st += st1
        return st
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})" 
    
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None,props)
    
    def to_html(self):
        if self.value ==None:
            raise ValueError("Leaf node has no value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag ==None:
            raise ValueError("tag is required")
        elif self.children ==None:
            raise ValueError("children is required")
        result = ""
        for child in self.children:
            result +=child.to_html()
        result = f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
        return result