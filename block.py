class Block:
    content = []
    start = []
    end = []

    # def __init__(self, content):
    #     self.content = []

    def save_start(self, index):
        self.start = index

    def save_end(self, index):
        self.end = index

    def length(self):
        return len(self.content)
