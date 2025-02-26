class Result:
    def __init__(self, graphs, class_freq, iterations, discrete):
        self.graphs = graphs
        self.class_freq = class_freq
        self.iterations = iterations
        self.discrete = discrete

    def __repr__(self):
        return ('(graphs={}, classes={}, iterations={}, is_discrete={})'
                .format(self.graphs, self.class_freq, self.iterations, self.discrete))

    def to_tuple(self):
        return self.graphs, self.class_freq, self.iterations, self.discrete

    def __lt__(self, other):
        return self.graphs < other.graphs
