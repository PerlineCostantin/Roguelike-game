import math

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
