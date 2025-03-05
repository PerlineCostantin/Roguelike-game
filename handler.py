import theGame
import random, copy
from Weapons import Weapons
from Armors import Armors


def heal(creature):
    if creature.hp + 3 <= creature.hpmax:  #ajout de l'impossibilité de se soigner si les hp du Héro sont au dessus des hp max
        creature.hp = creature.hp + 3
    else:
        creature.hp = creature.hpmax
    creature.poisoned = False  #utiliser une potion pour soigner le poison
    return True

def teleport(creature, unique): 
    """Teleport the creature"""
    k=random.choice(theGame.theGame()._floor._rooms).randEmptyCoord(theGame.theGame()._floor)
    x=theGame.theGame()._floor.pos(creature)
    m=k-x
    theGame.theGame()._floor.move(creature,m)
    return unique

def throw(power, loss): 
    """Throw an object"""
    pass

def nourish(creature): #pour nourir le Héro
    """Nourish Creature"""
    if creature.satiety==0:
        creature.satiety=20
    return True
    

def amuletGain(creature,xp,strength): #pour appliquer le pouvoir de l'amulette
    if xp is True:
        creature.xp+=3
    if strength is True:
        creature.strength+=2
    return True

def useStuff(self,nb,ty): #pour utiliser les Armes et les Armures
    if ty=="a":
        self.hp+=nb
    elif ty=="mw":
        self.strength+=nb
    



