import re
from itertools import product

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edge_weights = {}

    def add_edge(self, from_node, to_node, distance):
        self.nodes.update({from_node, to_node})
        self.edge_weights[(from_node, to_node)] = distance

    @property
    def edges(self):
        return self.edge_weights.keys()

    def _neighbors(self, source_node):
        for target_node in self.nodes:
            if (source_node, target_node) in self.edges:
                yield target_node

    @staticmethod
    def _edges_in_path(node_path):
        """ Returns edges (n0, n1), (n1, n2), ... from the node path """
        source_node, *target_nodes = node_path
        for target_node in target_nodes:
            yield (source_node, target_node)
            source_node = target_node

    @classmethod
    def from_string(cls, input):
        """ Build a graph from a list of 3-character strings of the form xyd,
            where x is the name of the source node, y is the name of the target
            node (both single letters), and d is the distance (integer 1-9).
        """
        graph = cls()
        for source, target, weight in re.findall('\w\w\d', input):
            graph.add_edge(source, target, int(weight))
        return graph

    def distance(self, node_path):
        """ Total distance along a path of nodes, or None if no such path exists """
        if len(node_path) < 2:
            return None

        try:
            return sum(self.edge_weights[edge] for edge in self._edges_in_path(node_path))
        except KeyError:  # missing an edge!
            return None

    def _longer_paths(self, node_path):
        """ Given a valid node path of length N, generate all valid node paths of length N+1 """
        for neighbor in self._neighbors(node_path[-1]):
            yield (*node_path, neighbor)

    def all_paths_from(self, source_node, max_distance=None, max_depth=None):
        """ Generate all paths starting at `source_node` given at least one of
            `max_weight` or `max_depth` (otherwise it could be unlimited)
        """
        if max_distance is None and max_depth is None:
            raise ValueError('At least one of max_distance or max_depth must be set')

        current_paths = [[source_node]]
        depth = 1
        while max_depth is None or depth <= max_depth:
            # generate all candidate paths of depth `depth`
            candidate_paths = []
            for valid_path in current_paths:
                candidate_paths += (path for path in self._longer_paths(valid_path)
                                         if max_distance is None or self.distance(path) <= max_distance)

            if not candidate_paths:  # no more valid paths at this depth
                return

            # return the paths we've generated at this depth, and move on to the next depth
            yield from candidate_paths
            current_paths = candidate_paths
            depth += 1

    def shortest_distance(self, source_node, target_node):
        if source_node == target_node:  # then Dijkstra's method fails (chooses the 0-length path)
            return self._shortest_distance_simple(source_node, target_node)
        return self._shortest_distance_dijkstra(source_node, target_node)

    def _shortest_distance_simple(self, source_node, target_node):
        """ Find the shortest distance (by total edge weight) between two nodes
            using an exhaustive search.
        """
        max_depth = len(self.nodes)  # no reasonable path would visit the same node twice
        distances = (self.distance(path) for path in self.all_paths_from(source_node, max_depth=max_depth)
                                         if path[-1] == target_node)
        return min(distances, default=None)

    def _shortest_distance_dijkstra(self, source_node, target_node):
        """ Use Dijkstra's algorithm to efficiently find the shortest distance between two distinct nodes """
        unvisited_nodes = self.nodes.copy()
        total_distance = {node: None for node in self.nodes}
        total_distance[source_node] = 0  # since we start here

        current_node = source_node
        while unvisited_nodes:
            # look at all the unvisited neighbors and update their distance if necessary
            for neighbor in unvisited_nodes.intersection(self._neighbors(current_node)):
                old_total = total_distance[neighbor]
                new_total = total_distance[current_node] + self.edge_weights[(current_node, neighbor)]
                if old_total is None or new_total < old_total:
                    total_distance[neighbor] = new_total

            # once we visit the target_node, we're done
            if current_node == target_node:
                return total_distance[target_node]
            # otherwise mark this node as visitied and contine on
            unvisited_nodes.remove(current_node)

            # now we choose the closest unvisited node to be the `current_node` and repeat
            reachable_nodes = (node for node in unvisited_nodes if total_distance[node] is not None)
            current_node = min(reachable_nodes, key=lambda node: total_distance[node], default=None)
            if not current_node:  # no available path!
                return None
