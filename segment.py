import numpy as np

class Segment:
    def __init__(self, im, label):
        self.im = im
        self.label = label

    def process(self):
        self.area = sum(sum(self.im))

	rows = np.any(self.im, axis=1)
        cols = np.any(self.im, axis=0)
        self.ymin, self.ymax = np.where(rows)[0][[0, -1]]
        self.xmin, self.xmax = np.where(cols)[0][[0, -1]]

    def get_center(self):
        return np.array([(self.xmin + self.xmax)/2, (self.ymin + self.ymax)/2])

    def get_elongation(self):
        return 1 - float(self.xmax - self.xmin + 1) / (self.ymax - self.ymin + 1) 

    def centrality(self):
        return np.linalg.norm(self.get_center() - np.array(self.im.shape)/2)

