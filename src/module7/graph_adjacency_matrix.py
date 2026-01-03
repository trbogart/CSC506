from typing import Optional, Iterator, Tuple

from module7.graph import Graph


class GraphAdjacencyMatrix[K, V](Graph):
    """
    Graph implemented with an adjacency matrix.
    All vertices must be added before any edge is added.
    Most of the logic is implemented in the Graph abstract base class
    """

    def __init__(self):
        super().__init__()

        # adjacency matrix uses weight or None if no path
        # 1 dimensional, use get_edge_index() to get index
        # empty until first edge is added
        self.matrix = list[Optional[float]]()

    def add_vertex(self, key: K, data: V = None) -> Optional[V]:
        if len(self.matrix) > 0:
            raise ValueError('Must add all vertices before any edges are added')
        return super().add_vertex(key, data)

    def add_edge(self, source_vertex: Graph.Vertex, dest_vertex: Graph.Vertex, weight: float = 1) -> None:
        """
        Adds a new directed edge to the graph.
        :param source_vertex: source vertex
        :param dest_vertex: destination vertex
        :param weight: weight of the edge (1 by default)
        """
        if len(self.matrix) == 0:
            self.matrix = [None] * (len(self.vertices) ** 2)
        self.matrix[self._get_edge_index(source_vertex, dest_vertex)] = weight

    def get_edge_weight(self, source_vertex: Graph.Vertex, dest_vertex: Graph.Vertex) -> Optional[float]:
        """
        Returns the weight of the edge between two vertices, or None if there is no edge.
        :param source_vertex: source vertex
        :param dest_vertex: destination vertex
        :return: weight of the edge, or None if there is no edge
        """
        if len(self.matrix) > 0:
            return self.matrix[self._get_edge_index(source_vertex, dest_vertex)]
        else:
            # special case for no edges added
            return None

    def get_edges_from_vertex(self, source_vertex: Graph.Vertex) -> Iterator[Tuple[Graph.Vertex, float]]:
        """
         Returns an iterator over all destination vertices and weights from the given vertex.
         Edges will be returned in the order that the target vertex was added.
         :param source_vertex: source vertex
         :return: an iterator, which may be empty, over all destination vertices and weights from this vertex
         """
        if len(self.matrix) > 0:
            for vertex in self.vertices.values():
                weight = self.get_edge_weight(source_vertex, vertex)
                if weight is not None:
                    yield vertex, weight

    def _get_edge_index(self, source_vertex: Graph.Vertex, dest_vertex: Graph.Vertex) -> int:
        return source_vertex.index * len(self.vertices) + dest_vertex.index
