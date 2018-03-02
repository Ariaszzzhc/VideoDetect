class Position:

    def __init__(self, x1=0, x2=0, y1=0, y2=0):
        self.x = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    @property
    def center(self):
        center_tuple = ((self.x + self.x2) / 2, (self.y1 + self.y2) / 2)
        return center_tuple


class Object:

    def __init__(self, id=-1, name='N/A', position=Position()):
        self.id = id
        self.name = name
        self.position = position

    def __str__(self):
        return "%d %s" % (self.id, self.name)


class ObjectList:
    def __init__(self):
        self.__objs = []

    def add_objects(self, objs_seqs):
        pass

    @property
    def data(self):
        return self.__objs
