# Class to create a sliding window for the ASN blocking algorithm. 
class Window:
    size = 0
    current = 0
    first = 0
    last = 0

    def __init__(self, size, first):
        self.size = size
        self.current = first
        self.first = first
        self.last = first + size - 1
