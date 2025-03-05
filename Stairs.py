from Element import Element
import theGame

class Stairs(Element):
    """ Strairs that goes down one floor. """

    def __init__(self):
        super().__init__("Stairs", 'E')

    def meet(self, hero):
        """Goes down"""
        theGame.theGame().buildFloor()
        theGame.theGame().alrdysleep=False
        theGame.theGame().addMessage("The " + hero.name + " goes down")
