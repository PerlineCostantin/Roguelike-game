from Element import Element
from Hero import Hero
import theGame
import copy

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
