from Element import Element
from Treasure import Treasure
import theGame

class Creature(Element):
    """A creature that occupies the dungeon.
        Is an Element. Has hit points and strength."""

    def __init__(self, name, hp, abbrv="", strength=1, xp=1, fast=False,poisoning=False):
        Element.__init__(self, name, abbrv)
        self.hp = hp
        self.strength = strength
        self.xp=xp
        self.fast = fast  #ajout des abilités des monstres (rapides, poison...)
        self.poisoning = poisoning
        self.poisoned = False
        self.hasKey = False
        self.key=False


    def description(self):
        """Description of the creature"""
        return Element.description(self) + "(" + str(self.hp) + ")"

    def meet(self, other):
        """The creature is encountered by an other creature.
            The other one hits the creature. Return True if the creature is dead."""
        if other.name=="Spirit": # Si le monstre est Spirit, le monstre apparait lorsqu'il est touché par le Héro
            other.abbrv="S"
            theGame.theGame().addMessage("An invisible creature is here")
        self.hp -= other.strength
        if other.poisoning: # Si le monstre empoisonne, le heros devient empoisonné
            self.poisoned = True  
        if other.hasKey: # Si le monstre posséde la clé, le Héro l'aura en tuant le monstre
            self.key = other.key
            theGame.theGame().addMessage("You are about to kill a "+other.name+" and get a treasure key")
        theGame.theGame().addMessage("The " + other.name + " hits the " + self.description())
        if self.hp > 0:
            return False
        if self.hp==0:
            other.xp+=self.xp
        return True
        
        

        
