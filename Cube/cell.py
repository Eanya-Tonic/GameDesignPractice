class Cell:
    def __init__(self, point=None, norm=None, color=None):
        self.point = point
        self.norm = norm
        self.color = color

    def __str__(self):
        return self.color