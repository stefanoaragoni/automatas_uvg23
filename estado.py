from set import Set

class Estado:
    def __init__(self, id, token=None, items_pre=None, items_post=None):
        self.id = id
        self.token = token
        self.items_pre = items_pre
        self.items_post = items_post