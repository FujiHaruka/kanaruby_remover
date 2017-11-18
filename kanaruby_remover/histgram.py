import math

class Histgram:
    def __init__(self, array, step=5):
        self.step = step
        self.min = min(array)
        self.max = max(array)
        self.total = len(array)
        self.size = math.floor((self.max - self.min) / step) + 1
        self.counts = [0 for i in range(self.size)]
        self.accum_counts = [0 for i in range(self.size)]
        self.sets = [[] for i in range(self.size)]
        for num in array:
            index = self.get_index(num)
            self.counts[index] += 1
            self.sets[index].append(num)
        for i, count in enumerate(self.counts):
            for j in range(i, self.size):
                self.accum_counts[j] += count

    def get_index(self, value):
        return math.floor((value - self.min) / self.step)

    def get_rate(self, value):
        index = self.get_index(value)
        accum_count = self.accum_counts[index]
        rate = accum_count / self.total
        return rate

    def get_nums(self, index):
        return self.sets[index]

    def __str__(self):
        return str(self.counts)

if __name__ == '__main__':
    from numpy.random import random_integers
    array = random_integers(0, 100, 100)
    hist = Histgram(array)
    print(hist)
    print(hist.get_rate(10))
    print(hist.get_nums(0))
