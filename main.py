from nltk.parse import CoreNLPParser
from tree import *

parser = CoreNLPParser('http://localhost:59000')

def parse_chinese(inputText):
    out = parser.parse(parser.tokenize(u'%s'%inputText))
    root = list(out)[0]
    root.pretty_print()
    output = root.pformat()
    return output

def get_children_list(node):
    out = []
    for ch in node.children:
        out.append(ch.value)
    return " ".join(out)

def get_leaves(node, output):
    if len(node.children) > 0:
        for ch in node.children:
            get_leaves(ch,output)
    else:
        output.append(node.value)


def get_all_leaves(node):
    output = []
    get_leaves(node,output)
    return output

def find_children(node,value):
    if node.value == value:
        return node
    else:
        found = None
        for ch in node.children:
            found = find_children(ch,value)
            if found is not None:
                return found 
        
        return None



def apply_reordering(node):

    if len(node.children) == 0:
        return 

    if len(node.children) == 1:
        apply_reordering(node.children[0])
        return 

    if node.value == "NP":
        if len(node.children) == 2:
            children = get_children_list(node)
            if children == "DNP NP": # ..的 NP --> NP ..的
                #print("FOUND")
                node.children = [node.children[1], node.children[0]]
            
            if children == "QP NP": # QP (两 只) NP (狗)
                node.children = [node.children[1], node.children[0]]
                noun = get_all_leaves(node.children[0])[-1]
                print(noun)
                node = find_children(node.children[1],"M")
                cl = node.children[0].value
                node.children[0].value = f"$CL({cl},{noun})"

   
    elif node.value == "DNP":  # DNP (NP (..) DEG (的) )
        if len(node.children) == 2:
            children = get_children_list(node)
            if children == "NP DEG": # NN 的 --> 的 NN
                node.children = [node.children[1], node.children[0]]
    
    for ch in node.children:
        apply_reordering(ch)

    return

out = parse_chinese("我有两百只狗。")
print(out)
y = get_penn_tree_from_string(out)
print(y[0].children[0].value)

apply_reordering(y[0].children[0])

output = []
get_leaves(y[0].children[0],output)
print(output)