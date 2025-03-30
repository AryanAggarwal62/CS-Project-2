""" This file parses the user profile data to generate a weighted graph"""

from typing import Any, Optional
import networkx as nx
import community

class Vertex:
    """A user vertex in a graph

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours
        - all(i>=0 for i in  self.neighbours.values())
    """

    item: Any
    neighbours: dict["Vertex", float]

    def __init__(self, item: Any, neighbours: Optional[dict["Vertex", float]] = None) -> None:
        """Initialize given vertex with item and self"""
        self.item = item
        self.neighbours = neighbours if neighbours is not None else {}


class WeightedGraph:
    """ A weighted graph of users

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """

    _vertices: dict[Any, Vertex]

    def __init__(self):
        """Initializing an empty graph"""
        self._vertices = {}

    def __getstate__(self):
        """Custom method to pickle only necessary data (no deep recursion)."""
        return {
            "vertices": {k: v.item for k, v in self._vertices.items()},
            "edges": [(v1.item, v2.item, weight) for v1 in self._vertices.values()
                      for v2, weight in v1.neighbours.items()]
        }

    def __setstate__(self, state):
        """Custom method to reconstruct graph from saved state."""
        self._vertices = {k: Vertex(k) for k in state["vertices"]}
        for v1, v2, weight in state["edges"]:
            self.add_edge(v1, v2, weight)

    def add_vertex(self, item: Any) -> None:
        """Adding a vertex to the graph without any edges"""

        if item not in self._vertices:
            self._vertices[item] = Vertex(item)

    def add_edge(self, item1: Any, item2: Any, weight: float) -> None:
        """Adding an edge between two items in the graph
        Raise ValueError if item1 or item2 are not in self._vertices
        """
        if item1 in self._vertices and item2 in self._vertices:
            self._vertices[item1].neighbours[self._vertices[item2]] = weight
            self._vertices[item2].neighbours[self._vertices[item1]] = weight
        else:
            raise ValueError

    def check_connected(self, user_1: Any, user_2: Any):
        """ Function returns if two vertices are directly connected in a graph otherwise raises a NameError"""
        if user_1 in self._vertices and user_2 in self._vertices:
            v1 = self._vertices[user_1]
            v2 = self._vertices[user_2]
            return v1 in self._vertices[user_2].neighbours and v2 in self._vertices[user_1].neighbours
        else:
            raise NameError

    def get_vertices(self):
        """returns all vertices in the graph"""
        return self._vertices

    def cluster(self) -> dict[Any, int]:
        """Cluster graph nodes into groups of similarity (user communities) using Louvain Method.

        Returns:
            A dictionary mapping each node to its assigned cluster.
        """

        nx_graph = nx.Graph()

        # add edges and weights
        for vertex in self._vertices.values():
            for neighbor, weight in vertex.neighbours.items():
                nx_graph.add_edge(vertex.item, neighbor.item, weight=weight)

        # apply clustering
        partition = community.best_partition(nx_graph, weight='weight')

        return partition

    def find_influential(self):
        """find influential players in the graph cluster
        Precondition:
            - graph is already in a clustered state
        """
        pass

    def dynamic_adjustment(self, node_1, node_2, new_weight):
        """change the weight between two nodes to new_weight"""
        pass


if __name__ == "__main__":
    """ have tests here"""
    pass
