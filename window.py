class Window:
    size = 0
    start = 0
    current = 0
    fst = 0
    lst = 0

    def __init__(self, size, start):
        self.size = size
        self.start = start
        self.current = start
        self.first = start
        self.last = start + size

    def first(self):
        return self.fst

    def last(self):
        return self.lst
