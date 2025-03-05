from Element import Element
import theGame
import random

#Nouvelle Classe du trésor 

class Treasure(Element):
    """A treasure located in a room. Can be opened with a key
    that the hero gets by defeating a random monster"""

    def __init__(self, name="treasure", abbrv="T"):
        Element.__init__(self,name,abbrv)
        self.opened = False
        a = theGame.theGame().equipments[int(2*theGame.theGame()._level)] #Beug (avec E) : quand le Hero veut changer de Floor, une erreur s'affiche
        self.content = a[random.randint(0,len(a)-1)]
        self.key = random.randint(0,50)

    def meet(self, other):
        if not self.opened and other.key==self.key:     # si le coffre n'a pas été ouvert et si le héro a la clé alors on peut prendre l'objet
            if other.take(self.content):    # si le héro a bien pu prendre l'objet
                self.opened = True          # le coffre est ouvert
                theGame.theGame().addMessage("You got a "+self.content.name+" from the treasure")
                self.content = None         # son contenu est alors vide
        else:
            print("Hero cannot open the Treasure. Hero must find the Key")
