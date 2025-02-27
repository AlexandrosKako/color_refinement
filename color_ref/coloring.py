from collections import Counter

from graph_utils.graph import Graph


class Coloring:
    def __init__(self, graph: Graph, graph_index):
        self.graph_index = graph_index
        self.graph = graph
        self.colors = {vertex: 1 for vertex in self.graph.vertices}
        self._iterations = -1
        self._previous_colors = None

    def sorted_classes(self):
        return sorted(self.colors.values())

    def class_freq(self):
        return list(Counter(self.colors.values()).values())

    def distinct_classes(self):
        return set(self.colors.values())

    def new_coloring(self):
        self._iterations += 1
        self._previous_colors = self.colors
        self.colors = {}

    def __repr__(self):
        return 'Coloring(graph={}, iteration={})'.format(self.graph_index, self._iterations)

    @property
    def iterations(self):
        return self._iterations

    @property
    def previous_colors(self):
        return self._previous_colors

    def color_class(self, vertex):
        return hash(tuple(sorted(Counter([self._previous_colors.get(n) for n in vertex.neighbours]).items())))

    def is_finished(self):
        return len(set(self.colors.values())) == len(set(self.previous_colors.values()))

    def is_discrete(self):
        return not any((c > 1) for c in self.class_freq())
