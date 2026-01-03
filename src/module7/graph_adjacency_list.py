from typing import Optional, Iterator, Tuple

from module7.graph import Graph


class GraphAdjacencyList[K, V](Graph):
    """
    Graph implemented with an adjacency list.
    Most of the logic is implemented in the Graph abstract base class.
    """

    def __init__(self):
        super().__init__()
        self.edges_by_source: dict[K, dict[K, float]] = {}

    def add_vertex(self, key: K, data: V = None) -> Optional[V]:
        vertex = super().add_vertex(key, data)

        # populate empty edge list after adding vertex
        self.edges_by_source[key] = {}
        return vertex

    def get_edge_weight(self, source_vertex: Graph.Vertex, dest_vertex: Graph.Vertex) -> Optional[float]:
        """
        Returns the weight of the edge between two vertices, or None if there is no edge.
        :param source_vertex: source vertex
        :param dest_vertex: destination vertex
        :return: weight of the edge, or None if there is no edge
        """
        return self.edges_by_source[source_vertex.key].get(dest_vertex.key, None)

    def add_edge(self, source_vertex: Graph.Vertex, dest_vertex: Graph.Vertex, weight: float = 1) -> None:
        """
        Adds a new directed edge to the graph.
        :param source_vertex: source vertex
        :param dest_vertex: destination vertex
        :param weight: weight of the edge (1 by default)
        """
        self.edges_by_source[source_vertex.key][dest_vertex.key] = weight

    def get_edges_from_vertex(self, source_vertex: Graph.Vertex) -> Iterator[Tuple[Graph.Vertex, float]]:
        """
         Returns an iterator over all destination vertices and weights from the given vertex.
         Edges will be returned in the order they were added.
         :param source_vertex: source vertex
         :return: an iterator, which may be empty, over all destination vertices and weights from this vertex
         """
        for key, weight in self.edges_by_source.get(source_vertex.key, {}).items():
            yield self.get_vertex(key), weight

    def edges_ordered(self) -> bool:
        """
        Returns true because edge order is preserved (used for testing).
        """
        return True
