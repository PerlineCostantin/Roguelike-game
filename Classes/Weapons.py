from Equipment import Equipment
from Creature import Creature
import theGame

#Nouvelle class pour les armes

class Weapons(Equipment):
    "Weapons !"
    def __init__(self,name,atk,abbrv="",usage=None,duree=5):
        Equipment.__init__(self,name,abbrv,usage,duree)
        self.atk=atk

    def use(self,creature): #pour utiliser l'arme
        theGame.theGame().addMessage(str(creature.name)+" equip the "+str(self.name))
        return self.usage(creature,self.atk)

