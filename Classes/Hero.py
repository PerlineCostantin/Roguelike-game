from Creature import Creature
from Equipment import Equipment
from Treasure import Treasure
from utils import getch

class Hero(Creature):
    """The hero of the game.
        Is a creature. Has an inventory of elements. """

    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2,satiety=20,action=0,level=1,hp_max=10,xp=0):
        Creature.__init__(self, name, hp, abbrv, strength, xp)
        self._inventory = []
        self.satiety=satiety  #ajout satiety du hero
        self.action=action
        self.level=level  #ajout level du hero
        self.hp_max=hp_max
        self.gold = 0
        

    def description(self):
        """Description of the hero"""
        return Creature.description(self) + str(self._inventory)

    def fullDescription(self):
        """Complete description of the hero"""
        res = ''
        for e in self.__dict__:
            if e[0] != '_':
                res += '> ' + e + ' : ' + str(self.__dict__[e]) + '\n'
        res += '> INVENTORY : ' + str([x.name for x in self._inventory])
        return res

    def checkEquipment(self, o):
        """Check if o is an Equipment."""
        if not isinstance(o, Equipment):
            raise TypeError('Not a Equipment')

    def take(self, elem): #Take renvoie désormais un booléen selon que l'item est effectivement pris ou non, le gold est stocké hors de l'inventaire, et la taille de l'inventaire ne doit pas dépasser 10
        """The hero takes adds the equipment to its inventory"""
        self.checkEquipment(elem)
        if elem.name == "Gold":     
            self.gold = self.gold + 1
            return True
        elif len(self._inventory) < 10:
            self._inventory.append(elem)  
            return True
        else:
            theGame.theGame().addMessage("Inventory is full")
            return False

    def throw(self, elem):  #Ajout de la méthode permettant de détruire un élément de son inventaire
        """The hero throws out an equipment of his inventory"""
        self._inventory.remove(elem)
        theGame().addMessage("You threw away the " + elem.name)

    def use(self, elem):
        """Use a piece of equipment"""
        if elem is None:
            return self.checkEquipment(elem)
        if elem not in self._inventory:
            raise ValueError('Equipment ' + elem.name + 'not in inventory')
        if elem.use(self):
            self._inventory.remove(elem)

    def nourriture(self):
        c=getch()
        if c in 'zqsd':
            self.action+=1
            if self.action%3==0:
                self.satiety-=1
                if self.satiety<=0:
                    self.satiety==0
                    self.hp-=1
                    
    def levelup(self):
        if self.xp>=2*self.level+5*(self.level)**2+3 :
            self.xp=0
            self.level+=1
            self.strength+=1
            self.hp_max+=2
            self.hp=self.hp_max
            theGame().addMessage("you're now level "+str(self.level))
