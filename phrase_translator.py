from utils.MultipleOutputFST_v06 import *
from utils.NameEntityTemplate import *

def load_dictionary(fname):
    fp = open(fname).readlines()
    dictItem = []
    for i in range(0,len(fp),5):
        dictItem.append((fp[i].strip(),fp[i+1].strip()+" "))
    return dictItem 

class PhraseTranslator():

    def __init__(self,modelfile):

        NED = NEDatabase()
        NEL = []
        NEL += [NE("England","LOC","อังกฤษ@LOC")]

        for item in NEL:
            NED.add(item)

        self.NED = NED
        self.root = MultipleOutputFST("ROOT")

        dictItem = load_dictionary(modelfile)
        for k in dictItem:
            self.root.addRule(k[0],k[1])


    def process(self,wordList,start):
        return self.root.process(wordList,start)

    def translate(self,sourceStr):
        return Translate(sourceStr,self.root,self.NED)


if __name__ == "__main__":
    translator = PhraseTranslator("dictionary/basic.txt")
    translator.translate("我 123")
