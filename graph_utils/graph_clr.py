from graph_utils.graph import Vertex, Graph

class VertexClr(Vertex):
    def __init__(self, graph: "Graph", label=None, color=None):
        super().__init__(graph, label)
        self.color = color

    def __repr__(self):
        """
        A programmer-friendly representation of the vertex.
        :return: The string to approximate the constructor arguments of the `Vertex'
        """
        return 'Vertex(label={}, #incident={}, color={})'.format(self.label, len(self._incidence), self.color)


class GraphClr(Graph):
    def __init__(self, directed: bool, n: int=0, simple: bool=False):
        self._v = list()
        self._e = list()
        self._simple = simple
        self._directed = directed
        self._next_label_value = 0

        for i in range(n):
            self.add_vertex(VertexClr(self, color=1))