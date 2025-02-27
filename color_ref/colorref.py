from coloring import Coloring
from result import Result
from graph_utils.graph_io import *
from collections import deque
import time


def basic_colorref(input):
    color_ref = ColorRef(input)
    return color_ref.run()

class ColorRef:
    def __init__(self, input):
        self.graphs = self.get_graphs_from_file(input)[0]
        self.coloring = {G: Coloring(G, index) for index, G in enumerate(self.graphs)}



    @staticmethod
    def get_graphs_from_file(path):
        file = path
        with open(file) as f:
            G = read_graph_list(Graph, f)
        return G

    def step(self):
        new_coloring = {}
        finished_coloring = {}
        for graph_coloring in self.coloring.values():
            self.step_for_graph(graph_coloring)
            if graph_coloring.is_finished():
                finished_coloring[graph_coloring.graph] = graph_coloring
            else:
                new_coloring[graph_coloring.graph] = graph_coloring
        return new_coloring, finished_coloring


    @staticmethod
    def step_for_graph(graph_coloring):
        graph_coloring.new_coloring()
        for v in graph_coloring.graph.vertices:
            new_color = graph_coloring.color_class(v)
            graph_coloring.colors[v] = new_color


    @staticmethod
    def formulate_results(colorings):
        eq_classes = {}
        for coloring in colorings.values():
            colors = tuple(coloring.sorted_classes())
            result = eq_classes.get(colors, None)
            if result is None:
                eq_classes[colors] = (
                    Result([coloring.graph_index], coloring.class_freq(), coloring.iterations, coloring.is_discrete()))
            else:
                result.add_graph(coloring.graph_index)
        return eq_classes.values()


    def run(self):
        finished_colorings = {}
        results = []
        while len(finished_colorings.keys()) < len(self.graphs):
            self.coloring, finished_coloring = self.step()
            if finished_coloring:
                results += (self.formulate_results(finished_coloring))
                finished_colorings.update(finished_coloring)
        return [r.to_tuple() for r in results]


if __name__=="__main__":
    start_time = time.time()
    results = basic_colorref('../benchmark_instances/CrefBenchmark6.grl')
    print(results)
    print("{} seconds".format(time.time() - start_time))