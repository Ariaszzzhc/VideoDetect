class Position:

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def center(self):
        center_tuple = (self.x + self.w / 2, self.y + self.h / 2)
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
