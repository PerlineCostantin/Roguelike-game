from Element import Element
import theGame

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
