import copy
import math
import random



def sign(x):
    if x > 0:
        return 1
    return -1



class Coord(object):
    """Implementation of a map coordinate"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '<' + str(self.x) + ',' + str(self.y) + '>'

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def distance(self, other):
        """Returns the distance between two coordinates."""
        d = self - other
        return math.sqrt(d.x * d.x + d.y * d.y)

    cos45 = 1 / math.sqrt(2)

    def direction(self, other):
        """Returns the direction between two coordinates.""" #modification methode et ajout de 4 directions en diagonale.
        if self.x<other.x and self.y<other.y :
            return Coord(-1,-1)
        elif self.x>other.x and self.y>other.y :
            return Coord(1,1)
        elif self.x>other.x and self.y<other.y :
            return Coord(1,-1)
        elif self.x<other.x and self.y>other.y :
            return Coord(1,-1)
        elif self.x==other.x and self.y<other.y:
            return Coord(0,-1)
        elif self.x==other.x and self.y>other.y:
            return Coord(0,1)
        elif self.x<other.x and self.y==other.y:
            return Coord(-1,0)
        elif self.x>other.x and self.y==other.y:
            return Coord(1,0)




class Element(object):
    """Base class for game elements. Have a name.
        Abstract class."""

    def __init__(self, name, abbrv=""):
        self.name = name
        if abbrv == "":
            abbrv = name[0]
        self.abbrv = abbrv

    def __repr__(self):
        return self.abbrv

    def description(self):
        """Description of the element"""
        return "<" + self.name + ">"

    def meet(self, hero):
        """Makes the hero meet an element. Not implemented. """
        raise NotImplementedError('Abstract Element')




class Equipment(Element):
    """A piece of equipment"""

    def __init__(self, name, abbrv="", usage=None,price=None): 
        Element.__init__(self, name, abbrv)
        self.usage = usage
        if price == None: #ajout  du prix des équipements (Merchant)
            price = 2
        self.price = price
        
    def meet(self, hero):
        """Makes the hero meet an element. The hero takes the element."""
        hero.take(self)
        theGame.theGame().addMessage("You pick up a " + self.name)
        return True

    def use(self, creature):
        """Uses the piece of equipment. Has effect on the hero according usage.
            Return True if the object is consumed."""
        if creature.satiety>0 and self.name in ["apple","pineapple","kiwi"]:  #Si le Hero n'a pas faim, il ne peut pas utiliser le fruit
            theGame.theGame().addMessage("The hero is full . "+"the "+self.name+" is not usable right now ")
            return False
        if self.usage is None : 
            theGame.theGame().addMessage("The " + self.name + " is not usable right ")
            return False
        else:
            theGame.theGame().addMessage("The " + creature.name + " uses the " + self.name)
            return self.usage(self, creature)


    
#Nouvelle class pour les armes

class Weapons(Equipment):
    "Weapons !"
    def __init__(self,name,atk,abbrv="",usage=None,duree=5):
        Equipment.__init__(self,name,abbrv,usage,duree)
        self.atk=atk

    def use(self,creature): #pour utiliser l'arme
        theGame.theGame().addMessage(str(creature.name)+" equip the "+str(self.name))
        return self.usage(creature,self.atk)



# Nouvelle Classe : Armures
class Armors(Equipment):
    """the Armors."""
    def __init__(self,name,prot,abbrv="",usage=None): 
        Equipment.__init__(self,name,abbrv,usage)
        self.prot=prot #point de protection

    def use(self,creature): #Equipe l'Armure au Hero
        theGame.theGame().addMessage(str(creature.name)+" equip the "+str(self.name))
        return self.usage(creature,self.prot)



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




#Nouvelle class du piège : placés alétoirement ils font perdre 2 hp
class Trap(Element):
    "Les Traps"

    def __init__(self,name="Trap",abbrv="."):
        Element.__init__(self, name, abbrv)

    def meet(self,other):
        other.hp-=2
        theGame.theGame().addMessage(str(other.name)+" walked on a trap and took damages")
        return True



class Stairs(Element):
    """ Strairs that goes down one floor. """

    def __init__(self):
        super().__init__("Stairs", 'E')

    def meet(self, hero):
        """Goes down"""
        theGame.theGame().buildFloor()
        theGame.theGame().alrdysleep=False
        theGame.theGame().addMessage("The " + hero.name + " goes down")



class Room(object):
    """A rectangular room in the map"""

    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return "[" + str(self.c1) + ", " + str(self.c2) + "]"

    def __contains__(self, coord):
        return self.c1.x <= coord.x <= self.c2.x and self.c1.y <= coord.y <= self.c2.y

    def intersect(self, other):
        """Test if the room has an intersection with another room"""
        sc3 = Coord(self.c2.x, self.c1.y)
        sc4 = Coord(self.c1.x, self.c2.y)
        return self.c1 in other or self.c2 in other or sc3 in other or sc4 in other or other.c1 in self

    def center(self):
        """Returns the coordinates of the room center"""
        return Coord((self.c1.x + self.c2.x) // 2, (self.c1.y + self.c2.y) // 2)

    def randCoord(self):
        """A random coordinate inside the room"""
        return Coord(random.randint(self.c1.x, self.c2.x), random.randint(self.c1.y, self.c2.y))

    def randEmptyCoord(self, map):
        """A random coordinate inside the room which is free on the map."""
        c = self.randCoord()
        while map.get(c) != Map.Map.ground or c == self.center():
            c = self.randCoord()
        return c

    def decorate(self, map):
        """Decorates the room by adding a random equipment and monster."""
        map.put(self.randEmptyCoord(map), theGame.theGame().randEquipment())
        map.put(self.randEmptyCoord(map), theGame.theGame().randMonster())
        
        for t in range(0,random.randint(0,4)):                    #ajout de pièges (nombre et placement aléatoire)
            map.put(self.randEmptyCoord(map),Trap())




class Map(object):
    """A map of a game .
       Contains game elements."""


    ground = '.'  # A walkable ground cell
    dir = {'z': Coord(0, -1), 's': Coord(0, 1), 'd': Coord(1, 0), 'q': Coord(-1, 0), 'e': Coord(1, 1), 'a': Coord(-1, -1), 'w': Coord(-1, 1), 'c': Coord(1, -1)}  #8 directions
    empty = ' '  # A non walkable cell


    def __init__(self, size=20, hero=None, coffre="N"): # initialisation des éléments de la Map
        self._mat = []
        self._elem = {}
        self._rooms = []
        self._roomsToReach = []
        for i in range(size):
            self._mat.append([Map.empty] * size)
        if hero is None:
            hero = Hero()
        self._hero = hero
        self.generateRooms(7)
        self.reachAllRooms()
        self.put(self._rooms[0].center(), hero)
        for r in self._rooms:
            r.decorate(self)
        self.putMerchant()
        self.key = self.putTreasure()
        self.giveMonsterTkey()

        
    def addRoom(self, room): # ajoute une piéce (room) dans la Map
        """Adds a room in the map."""
        self._roomsToReach.append(room)
        for y in range(room.c1.y, room.c2.y + 1):
            for x in range(room.c1.x, room.c2.x + 1):
                self._mat[y][x] = Map.ground

    def findRoom(self, coord):  
        """If the coord belongs to a room, returns the room elsewhere returns None"""
        for r in self._roomsToReach:
            if coord in r:
                return r
        return None

    def intersectNone(self, room):
        """Tests if the room shall intersect any room already in the map."""
        for r in self._roomsToReach:
            if room.intersect(r):
                return False
        return True

    def dig(self, coord):
        """Puts a ground cell at the given coord.
            If the coord corresponds to a room, considers the room reached."""
        self._mat[coord.y][coord.x] = Map.ground
        r = self.findRoom(coord)
        if r:
            self._roomsToReach.remove(r)
            self._rooms.append(r)

    def corridor(self, cursor, end):
        """Digs a corridors from the coordinates cursor to the end, first vertically, then horizontally."""
        d = end - cursor
        self.dig(cursor)
        while cursor.y != end.y:
            cursor = cursor + Coord(0, sign(d.y))
            self.dig(cursor)
        while cursor.x != end.x:
            cursor = cursor + Coord(sign(d.x), 0)
            self.dig(cursor)

    def reach(self):
        """Makes more rooms reachable.
            Start from one random reached room, and dig a corridor to an unreached room."""
        roomA = random.choice(self._rooms)
        roomB = random.choice(self._roomsToReach)

        self.corridor(roomA.center(), roomB.center())

    def reachAllRooms(self):
        """Makes all rooms reachable.
            Start from the first room, repeats @reach until all rooms are reached."""
        self._rooms.append(self._roomsToReach.pop(0))
        while len(self._roomsToReach) > 0:
            self.reach()

    def randRoom(self):
        """A random room to be put on the map."""
        c1 = Coord(random.randint(0, len(self) - 3), random.randint(0, len(self) - 3))
        c2 = Coord(min(c1.x + random.randint(3, 8), len(self) - 1), min(c1.y + random.randint(3, 8), len(self) - 1))
        return Room(c1, c2)

    def generateRooms(self, n):
        """Generates n random rooms and adds them if non-intersecting."""
        for i in range(n):
            r = self.randRoom()
            if self.intersectNone(r):
                self.addRoom(r)

    def __len__(self):
        return len(self._mat)

    def __contains__(self, item):
        if isinstance(item, Coord):
            return 0 <= item.x < len(self) and 0 <= item.y < len(self)
        return item in self._elem

    def __repr__(self):
        s = ""
        for i in self._mat:
            for j in i:
                s += str(j)
            s += '\n'
        return s

    def checkCoord(self, c):
        """Check if the coordinates c is valid in the map."""
        if not isinstance(c, Coord):
            raise TypeError('Not a Coord')
        if not c in self:
            raise IndexError('Out of map coord')

    def checkElement(self, o):
        """Check if o is an Element."""
        if not isinstance(o, Element):
            raise TypeError('Not a Element')

    def put(self, c, o):
        """Puts an element o on the cell c"""
        self.checkCoord(c)
        self.checkElement(o)
        if o in self._elem:
            raise KeyError('Already placed')
        self._mat[c.y][c.x] = o
        self._elem[o] = c

    def get(self, c):
        """Returns the object present on the cell c"""
        self.checkCoord(c)
        return self._mat[c.y][c.x]

    def pos(self, o):
        """Returns the coordinates of an element in the map """
        self.checkElement(o)
        return self._elem[o]

    def rm(self, c):
        """Removes the element at the coordinates c"""
        self.checkCoord(c)
        del self._elem[self._mat[c.y][c.x]]
        self._mat[c.y][c.x] = Map.ground

    def move(self, e, way):
        """Moves the element e in the direction way."""
        orig = self.pos(e)
        dest = orig + way
        if dest in self:
            if self.get(dest) == Map.ground:
                self._mat[orig.y][orig.x] = Map.ground
                self._mat[dest.y][dest.x] = e
                self._elem[e] = dest
            elif self.get(dest) != Map.empty and self.get(dest).meet(e) and self.get(dest) != self._hero:
                self.rm(dest)

    def putMerchant(self):  #nouvelle methode : place le marchant au centre d'une salle
        a = list(self._rooms)
        a.pop(0)
        c = random.choice(a).center()
        self.put(c,Merchant("Merchant"))

    def putTreasure(self):  #nouvelle methode : place le trésor aléatoirement
        a = list(self._rooms)
        a.pop(0)
        c = random.choice(a).randEmptyCoord(self)
        treasure = Treasure()
        self.put(c,treasure)
        return treasure.key

    def giveMonsterTkey(self):  #nouvelle methode : qui donne la clé du trésor a un monstre quelconque
        l = list(self._elem.keys())
        m = random.choice(l)
        while isinstance(m,Hero) or not isinstance(m,Creature):
            m = random.choice(l)
        print(m.name,self.pos(m),"has key")
        m.key = self.key
        m.hasKey = True
        
    def moveAllMonsters(self):
        """Moves all monsters in the map.
            If a monster is at distance lower than 6 from the hero, the monster advances."""
        h = self.pos(self._hero)
        for e in self._elem:
            c = self.pos(e)
            if (isinstance(e, Creature) and not(isinstance(e,Trap)) and e != self._hero and c.distance(h) < 6):
                d = c.direction(h)
                if self.get(c + d) in [Map.ground, self._hero] : # Beug(rare): on ne trouve pas les conditions nécessaires pour un déplacement en diagonale des monstres
                    self.move(e, d)
                    if e.fast:
                            self.move(e, d) # Si le monstre est rapide il se deplace deux fois
                

   

#Nouvelle class du marchant

class Merchant(Element):
    def __init__(self,name,abbrv=""):
        Element.__init__(self,name,abbrv)
        self.merchantprices()
   
    def merchantprices(self):
        self.prices = {}
        for i in theGame.theGame().equipments.values():
            for j in i:
                if j.name!="Gold":
                    self.prices[j.name] = j.price
                   
    def meet(self,other):
        if not isinstance(other,Hero):
            return False
        print("Welcome to my Shop")
        print("Availbale Equipments : " + str(self.prices))
        item = input("What do you want to buy ? ")
        for e in theGame.theGame().equipments.values():
            for f in e:
                if f.name == item:
                    item = copy.copy(f)
        if len(other._inventory)<10 and other.gold>=self.prices[item.name]:
            other.buy(item,self.prices[item.name],self)
        else:
            print("I'm sorry you can't afford this.")




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

    """ available actions """
    _actions = {'z': lambda h: theGame.theGame()._floor.move(h, Coord(0, -1)), \
                'q': lambda h: theGame.theGame()._floor.move(h, Coord(-1, 0)), \
                's': lambda h: theGame.theGame()._floor.move(h, Coord(0, 1)), \
                't': lambda hero: hero.throw(theGame().select(hero._inventory)),\
                'd': lambda h: theGame.theGame()._floor.move(h, Coord(1, 0)), \
                'e': lambda h: theGame.theGame()._floor.move(h, Coord(1, 1)),\   #nouveaux deplacement en diagonale
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
            
    def repos(self): #nouvelle methode qui permet de gagner 5 hp une fois par niveau
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
                self._hero.hp -= 1  #Vérification du poison a chaque tour de jeu
            
        print("--- Game Over ---")





theGame.theGame().play()

def theGame(game=Game()):
    """Game singleton"""
    return game





def getch():
    """Single char input, only works only on mac/linux/windows OS terminals"""
    try:
        import termios
        # POSIX system. Create and return a getch that manipulates the tty.
        import sys, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch().decode('utf-8')

