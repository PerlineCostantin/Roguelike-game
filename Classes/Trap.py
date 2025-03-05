from Element import Element
import theGame


#Nouvelle class du piège : placés alétoirement ils font perdre 2 hp
class Trap(Element):
    "Les Traps"

    def __init__(self,name="Trap",abbrv="."):
        Element.__init__(self, name, abbrv)

    def meet(self,other):
        other.hp-=2
        theGame.theGame().addMessage(str(other.name)+" walked on a trap and took damages")
        return True
