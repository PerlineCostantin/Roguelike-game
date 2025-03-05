from Equipment import Equipment
import theGame

# Nouvelle Classe : Armures
class Armors(Equipment):
    """the Armors."""
    def __init__(self,name,prot,abbrv="",usage=None): 
        Equipment.__init__(self,name,abbrv,usage)
        self.prot=prot #point de protection

    def use(self,creature): #Equipe l'Armure au Hero
        theGame.theGame().addMessage(str(creature.name)+" equip the "+str(self.name))
        return self.usage(creature,self.prot)
