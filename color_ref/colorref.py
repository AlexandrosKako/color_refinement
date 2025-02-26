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
        self._max_color = 1
        self.graphs = self.get_graphs_from_file(input)[0]
        self.coloring = {G: Coloring(G, index) for index, G in enumerate(self.graphs)}



    @staticmethod
    def get_graphs_from_file(path):
        file = path
        with open(file) as f:
            G = read_graph_list(Graph, f)
        return G

    def step(self):
        color_classes = {}
        new_coloring = {}
        finished_coloring = {}
        for graph_coloring in self.coloring.values():
            self.step_for_graph(color_classes, graph_coloring)
            if graph_coloring.is_finished():
                finished_coloring[graph_coloring.graph] = graph_coloring
            else:
                new_coloring[graph_coloring.graph] = graph_coloring
        return new_coloring, finished_coloring


    def step_for_graph(self, color_classes, graph_coloring):
        graph_coloring.new_coloring()
        for v in graph_coloring.graph.vertices:
            color = graph_coloring.previous_colors.get(v)
            color_class = graph_coloring.color_class(v)
            graph_coloring.colors[v] = self.update_coloring(color, color_class, color_classes, v)


    def update_coloring(self, color, color_class, color_classes, v):
        if color in color_classes.values():
            color = color_classes.get(color_class, None)
            if color is None:
                self._max_color += 1
                color_classes[color_class] = self._max_color
                return self._max_color
            else:
                return color
        else:
            color_classes[color_class] = color
            return color


    def equivalence_classes(self, colorings):
        graphs_to_classify = deque(colorings.keys())
        graph = graphs_to_classify.popleft()
        class_representatives = [graph]
        classes = [[colorings.get(graph).graph_index]]
        while graphs_to_classify:
            graph = graphs_to_classify.popleft()
            isClassified = False
            for index, representative in enumerate(class_representatives):
                coloring = colorings.get(graph)
                if coloring.sorted_classes() == colorings.get(representative).sorted_classes():
                    classes[index].append(coloring.graph_index)
                    isClassified = True
                    break

            if not isClassified:
                classes.append([coloring.graph_index])
                class_representatives.append(graph)
        return classes


    def formulate_results(self, finished_coloring):
        classes = self.equivalence_classes(finished_coloring)
        results = []
        for members in classes:
            coloring = finished_coloring.get(self.graphs[members[0]])
            results.append(Result(members, coloring.class_freq(), coloring.iterations, coloring.is_discrete()))
        return sorted(results)


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
    results = basic_colorref('../benchmark_instances/CrefBenchmark4.grl')
    print(results)
    print("{} seconds".format(time.time() - start_time))