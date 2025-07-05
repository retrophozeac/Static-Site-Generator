class HTMLNode:
    def __init__(self,tag:str =None,value:str=None,children=None,props:dict=None):
        self.tag = tag
        self.value =value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        st = ""
        for key, value in self.props.items():
            st1 = " "+key +"=\""+value +"\""
            st += st1
        return st
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})" 