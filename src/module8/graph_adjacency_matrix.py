import itertools
from array import array
from typing import Optional, Iterator, Tuple

from module8.graph import Graph


class GraphAdjacencyMatrix[K, V](Graph[K, V]):
    """
    Graph implemented with an adjacency matrix.
    All vertices must be added before any edge is added.
    Most of the logic is implemented in the Graph abstract base class
    """

    def __init__(self):
        super().__init__()

        # adjacency matrix uses weight or None if no path
        # 1 dimensional, use get_edge_index() to get index
        # None until first edge is added
        self.adjacency_matrix = None

    def add_vertex(self, key: K, data: V = None) -> Optional[V]:
        # verify that vertices are added before edges (so matrix can be allocated with proper size)
        if self.adjacency_matrix is not None:
            raise ValueError('Must add all vertices before any edges are added')
        return super().add_vertex(key, data)

    def add_edge(self, source_vertex: Graph.Vertex, dest_vertex: Graph.Vertex, weight: float = 1.0) -> None:
        """
        Adds a new directed edge to the graph.
        :param source_vertex: source vertex
        :param dest_vertex: destination vertex
        :param weight: weight of the edge (1 by default)
        """
        if self.adjacency_matrix is None:
            # initialize matrix if this is the first edge added
            # Note: use array module for better efficiency, at the cost of needing to convert 'inf' to None.
            self.adjacency_matrix = array('f', itertools.repeat(float('inf'), len(self.vertices) ** 2))
        # set edge weight
        # convert 2d square index to 1d index using _get_edge_index
        self.adjacency_matrix[self._get_edge_index(source_vertex, dest_vertex)] = weight

    def get_edge_weight(self, source_vertex: Graph.Vertex, dest_vertex: Graph.Vertex) -> Optional[float]:
        """
        Returns the weight of the edge between two vertices, or None if there is no edge.
        :param source_vertex: source vertex
        :param dest_vertex: destination vertex
        :return: weight of the edge, or None if there is no edge
        """
        if self.adjacency_matrix is not None:
            # convert 2d square index to 1d index using _get_edge_index
            weight = self.adjacency_matrix[self._get_edge_index(source_vertex, dest_vertex)]
            return weight if weight != float('inf') else None
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
        if self.adjacency_matrix is not None:
            base_index = self._get_base_index(source_vertex)
            for dest_vertex in self.vertices.values():
                weight = self.adjacency_matrix[base_index + dest_vertex.index]
                if weight != float('inf'):
                    yield dest_vertex, weight

    def edges_ordered(self) -> bool:
        """
        Returns false because edge order is not preserved.
        Used for testing.
        """
        return False

    def _get_edge_index(self, source_vertex: Graph.Vertex, dest_vertex: Graph.Vertex) -> int:
        return self._get_base_index(source_vertex) + dest_vertex.index

    def _get_base_index(self, source_vertex: Graph.Vertex) -> int:
        return source_vertex.index * len(self.vertices)
