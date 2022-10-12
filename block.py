class Block:
    start = 0
    end = 0

    # def __init__(self, content):
    #     self.content = []

    def save_start(self, index):
        self.start = index

    def save_end(self, index):
        self.end = index

    def length(self):
        return self.end - self.start
