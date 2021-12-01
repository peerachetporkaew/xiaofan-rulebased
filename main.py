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
   
    elif node.value == "DNP":  # DNP (NP (..) DEG (的) )
        if len(node.children) == 2:
            children = get_children_list(node)
            if children == "NP DEG": # NN 的 --> 的 NN
                node.children = [node.children[1], node.children[0]]
    
    for ch in node.children:
        apply_reordering(ch)

    return


def get_leaves(node, output):
    if len(node.children) > 0:
        for ch in node.children:
            get_leaves(ch,output)
    else:
        output.append(node.value)



out = parse_chinese("父親的母親")
print(out)
y = get_penn_tree_from_string(out)
print(y[0].children[0].value)

apply_reordering(y[0].children[0])

output = []
get_leaves(y[0].children[0],output)
print(output)



