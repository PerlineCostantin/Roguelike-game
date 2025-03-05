from Equipment import Equipment
from Creature import Creature
from Coord import Coord
from Hero import Hero
from Map import Map
from Trap import Trap
from Stairs import Stairs
from Merchant import Merchant
from Element import Element
from Treasure import Treasure
from Armors import Armors
from handler import heal, teleport, nourish, throw, useStuff, amuletGain
from Weapons import Weapons
from utils import getch
import theGame
import random, copy

class Game(object):
    """ Class representing game state """

    """ available equipments """
    equipments = {0: [Armors("chainmail",prot=2,usage=lambda creature,prot : useStuff(creature,nb=prot,ty="a")), Weapons("pistol",atk=1,abbrv="i",usage=lambda creature,atk : useStuff(creature,nb=atk,ty="mw")),Equipment("potion", "!", usage=lambda self, hero: heal(hero)), \
                      Equipment("gold", "o"), \
                      Equipment("apple", "a", usage=lambda self, hero: nourish(hero)), Equipment("pineapple", "p", usage=lambda self, hero: nourish(hero)),Equipment("kiwi", "k", usage=lambda self, hero: nourish(hero))], \
                  1: [Armors("helmet",prot=3,usage=lambda creature,prot : useStuff(creature,nb=prot,ty="a")), Equipment("hehe", "h", usage=lambda self, hero: teleport(hero, True)),Weapons("sword",atk=2,abbrv='s',usage=lambda creature,atk : useStuff(creature,nb=atk,ty="mw")), Equipment("Ruby", "r", usage=lambda self, hero: amuletGain(hero,False,True)),Equipment("Topaz", "t", usage=lambda self, hero: amuletGain(hero,True,False))], \
                  2: [Equipment("bow", usage=lambda self, hero: throw(1, True)), Armors("boots",prot=1,usage=lambda creature,prot : stuff(creature,empl=2,nb=prot,ty="a"))], \
                  3: [Equipment("portoloin", "w", usage=lambda self, hero: teleport(hero, False))], \
                  }
    """ available monsters """
    monsters = {0: [Creature("Goblin", 4, fast=True,poisoning=True), Creature("Bat", 2, "W", fast=True)],
                1: [Creature("Ork", 6, strength=2, xp=3,poisoning=True), Creature("Blob", 10, xp=2), Creature("Spirit",8,'.', xp=2)], 5: [Creature("Dragon", 20, strength=3, xp=40)],
                }

    """ available actions """ #nouveaux deplacement en diagonale "e" "a" "w" "c"
    _actions = {'z': lambda h: theGame.theGame()._floor.move(h, Coord(0, -1)), \
                'q': lambda h: theGame.theGame()._floor.move(h, Coord(-1, 0)), \
                's': lambda h: theGame.theGame()._floor.move(h, Coord(0, 1)), \
                't': lambda hero: hero.throw(theGame().select(hero._inventory)),\
                'd': lambda h: theGame.theGame()._floor.move(h, Coord(1, 0)), \
                'e': lambda h: theGame.theGame()._floor.move(h, Coord(1, 1)),\
                'a': lambda h: theGame.theGame()._floor.move(h, Coord(-1, -1)), \
                'w': lambda h: theGame.theGame()._floor.move(h, Coord(-1, 1)), \
                'c': lambda h: theGame.theGame()._floor.move(h, Coord(1, -1)), \
                'i': lambda h: theGame.theGame().addMessage(h.fullDescription()), \
                'k': lambda h: h.__setattr__('hp', 0), \
                'u': lambda h: h.use(theGame.theGame().select(h._inventory)), \
                ' ': lambda h: None, \
                'h': lambda hero: theGame.theGame().addMessage("Available actions : " + str(list(Game._actions.keys()))), \
                'b': lambda hero: theGame.theGame().addMessage("I am " + hero.name), \
                'r': lambda hero : theGame.theGame().repos()
                }

    def __init__(self, level=1, hero=None):
        self._level = level
        self._messages = []
        if hero == None:
            hero = Hero()
        self._hero = hero
        self._floor = None
        self.alrdysleep=False
        

    def buildFloor(self):
        """Creates a map for the current floor."""
        print("--- Welcome Hero! ---")
        self._floor = Map(hero=self._hero)
        self._floor.put(self._floor._rooms[-1].center(), Stairs())
        self._level += 1

    def addMessage(self, msg):
        """Adds a message in the message list."""
        self._messages.append(msg)

    def readMessages(self):
        """Returns the message list and clears it."""
        s = ''
        for m in self._messages:
            s += m + '. '
        self._messages.clear()
        return s

    def randElement(self, collect):
        """Returns a clone of random element from a collection using exponential random law."""
        x = random.expovariate(1 / self._level)
        for k in collect.keys():
            if k <= x:
                l = collect[k]
        return copy.copy(random.choice(l))

    def randEquipment(self):
        """Returns a random equipment."""
        return self.randElement(Game.equipments)

    def randMonster(self):
        """Returns a random monster."""
        return self.randElement(Game.monsters)

    def select(self, l):
        print("Choose item> " + str([str(l.index(e)) + ": " + e.name for e in l]))
        c = getch()
        if c.isdigit() and int(c) in range(len(l)):
            return l[int(c)]
            
    def repos(self): #nouvelle methode qui permet de gagner 5 hp une fois par salle
        if not(self.alrdysleep):
            self.alrdysleep=True
            self._hero.hp+=5
            if self._hero.hp>=self._hero.hp_max:
                self._hero.hp=self._hero.hp_max
            for i in range(9):
                self._floor.moveAllMonsters()
            theGame.theGame().addMessage("Welcome back !")
        else :
            theGame.theGame().addMessage("too sleepy ...?")

            
    def play(self):
        """Main game loop"""
        self.buildFloor()
        while self._hero.hp > 0:
            print()
            print(self._floor)
            print(self._hero.description())
            print(self.readMessages())
            c = getch()
            if c in Game._actions:
                Game._actions[c](self._hero)
            self._floor.moveAllMonsters()
            self._hero.nourriture()
            if self._hero.poisoned:
                self._hero.hp -= 1  #vérification du poison a chaque tour de jeu
            
        print("--- Game Over ---")

    

    
    
