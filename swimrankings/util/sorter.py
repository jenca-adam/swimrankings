import heapq


class Sorter:
    def __init__(self, keyf=None):
        self.keyf = keyf or (lambda a: a)
        self.heap = []

    def feed(self, item):
        heapq.heappush(self.heap, (self.keyf(item), id(item), item))  # hacky

    def extract(self):
        # destroys the heap
        return [heapq.heappop(self.heap)[-1] for _ in range(len(self.heap))]
