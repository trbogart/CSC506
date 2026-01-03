from abc import ABC, abstractmethod
from collections import deque
from typing import Optional, Iterator, Tuple


class Graph[K, V](ABC):
    """
    Abstract base class for graph implementations.
    """

    class Vertex:
        """
        Vertex in a graph. The key and index should not be modified.
        """

        def __init__(self, key: K, index: int, value: V = None):
            self.key = key
            self.index = index
            self.value = value

        def __str__(self):
            return f'Vertex(key: {self.key}, index: {self.index}, value: {self.value})'

        def __repr__(self):
            return f'Vertex(key: {repr(self.key)}, index: {self.index}, value: {repr(self.value)})'

    def __init__(self):
        self.vertices = dict[K, Graph.Vertex]()  # key -> data

    def __contains__(self, key: K):
        """
        Returns true if there is a vertex with the given key.
        """
        return key in self.vertices

    def add_vertex(self, key: K, data: V = None) -> Vertex:
        """
        Adds a new vertex to the graph.
        :param key: key to add
        :param data: data to add
        :return: the vertex
        :raises KeyError: if vertex with given key already exists
        """
        if key in self.vertices:
            raise KeyError(f'Vertex with key {key} already found in graph')
        vertex = self.Vertex(key, len(self.vertices), data)
        self.vertices[key] = vertex
        return vertex

    def get_vertex(self, key: K) -> Optional[Vertex]:
        """
        Returns the vertex with the given key.
        :param key: key to check
        :return: the vertex with the given key
        """
        if key in self.vertices:
            return self.vertices[key]
        return None

    def add_edge_undirected(self, vertex1: Vertex, vertex2: Vertex, weight: float = 1.0) -> None:
        """
        Adds a new undirected edge to the graph. Can use either vertex objects or keys.
        :param vertex1: first vertex
        :param vertex2: second vertex
        :param weight: weight of the edge (1.0 by default)
        """
        # verify that both keys exist
        self.add_edge(vertex1, vertex2, weight)
        self.add_edge(vertex2, vertex1, weight)

    @abstractmethod
    def add_edge(self, from_vertex: Vertex, to_vertex: Vertex, weight: float = 1.0) -> None:
        """
        Adds a new directed edge to the graph. Can use either vertex objects or keys.
        :param from_vertex: key of the source vertex
        :param to_vertex: key of the destination vertex
        :param weight: weight of the edge (1.0 by default)
        :raises KeyError: if vertices with given keys have not been added
        """
        pass

    @abstractmethod
    def get_edge_weight(self, from_vertex: Vertex, to_vertex: Vertex) -> Optional[float]:
        """
        Returns the weight of the edge between two vertices, or None if there is no edge.
        :param from_vertex: source vertex
        :param to_vertex: destination vertex
        :return: weight of the edge, or None if there is no edge
        :raises KeyError: if vertices with given keys have not been added
        """

    @abstractmethod
    def get_edges_from_vertex(self, from_vertex: Vertex) -> Iterator[Tuple[Vertex, float]]:
        """
        Returns an iterator over all destination vertices and weights from the given vertex.
        :param from_vertex: source vertex
        :return: an iterator, which may be empty, over all destination vertex keys and weights from this vertex
        """
        pass

    def traverse_depth_first(self, root_vertex: Optional[Vertex] = None) -> Iterator[Vertex]:
        """
        Do a depth-first traversal.
        :param root_vertex: root vertex, or None to traverse all vertices.
        :return: depth-first iterator over vertices
        :raises KeyError: if root key given and vertex with given root key has not been added
        """
        visited = set[self.Vertex]()
        if root_vertex is None:
            # iterate all vertices
            for vertex in self.vertices.values():
                yield from self._traverse_depth_first(vertex, visited)
        else:
            yield from self._traverse_depth_first(root_vertex, visited)

    def _traverse_depth_first(self, vertex: Vertex, visited: set[Vertex]) -> Iterator[Vertex]:
        """
        Internal method to do a depth-first traversal of subgraph for given vertex.
        :param vertex: vertex to traverse
        :param visited: vertex keys that have already been visited
        :return: depth-first iterator over vertices
        """
        if vertex not in visited:
            visited.add(vertex)
            for to_vertex_key, _ in self.get_edges_from_vertex(vertex):
                yield from self._traverse_depth_first(to_vertex_key, visited)
            yield vertex

    def traverse_breadth_first(self, vertex: Vertex) -> Iterator[Vertex]:
        """
        Do a breadth-first traversal of all vertices.
        :param vertex: key of the root vertex.
        :return: breadth-first iterator over vertices
        """
        discovered = {vertex}
        queue = deque[Graph.Vertex]()
        queue.append(vertex)
        while len(queue) > 0:
            vertex = queue.popleft()
            yield vertex
            for to_vertex, _ in self.get_edges_from_vertex(vertex):
                if to_vertex not in discovered:
                    discovered.add(to_vertex)
                    queue.append(to_vertex)

    def shortest_path(self, start_vertex: Vertex, end_vertex: Vertex) -> list[Vertex]:
        """
        Returns the shortest path between two vertices, or an empty list if there is no path.
        :param start_vertex: start vertex
        :param end_vertex: end vertex
        :return: list containing the shortest path from start vertex to end vertex, or empty if none
        """
        # Dijkstra's algorithm
        unvisited = list[Graph.Vertex]()
        for current_vertex in self.vertices.values():
            unvisited.append(current_vertex)

        distances = [float('inf')] * len(self.vertices)
        pred_vertices: list[Optional[Graph.Vertex]] = [None] * len(self.vertices)

        distances[start_vertex.index] = 0.0

        while len(unvisited) > 0:
            # visit vertex with minimum distance from start_vertex
            smallest_index = 0

            for i in range(1, len(unvisited)):
                if distances[unvisited[i].index] < distances[unvisited[smallest_index].index]:
                    smallest_index = i
            current_vertex = unvisited.pop(smallest_index)

            for adj_vertex, edge_weight in self.get_edges_from_vertex(current_vertex):
                alternative_path_distance = distances[current_vertex.index] + edge_weight

                if alternative_path_distance < distances[adj_vertex.index]:
                    distances[adj_vertex.index] = alternative_path_distance
                    pred_vertices[adj_vertex.index] = current_vertex

        # now work backwards to find the shortest path
        path = []
        if pred_vertices[end_vertex.index] is None:
            # no path
            return path

        current_vertex = end_vertex
        while current_vertex is not start_vertex:
            path.append(current_vertex)
            current_vertex = pred_vertices[current_vertex.index]
        path.append(start_vertex)
        path.reverse()
        return path


class GraphAdjacencyList[K, V](Graph):
    """
    Graph implemented with an adjacency list.
    """

    def __init__(self):
        super().__init__()
        self.edges_by_source: dict[K, dict[K, float]] = {}

    def add_vertex(self, key: K, data: V = None) -> Optional[V]:
        vertex = super().add_vertex(key, data)
        self.edges_by_source[key] = {}
        return vertex

    def get_edge_weight(self, from_vertex: Graph.Vertex, to_vertex: Graph.Vertex) -> Optional[float]:
        return self.edges_by_source[from_vertex.key].get(to_vertex.key, None)

    def add_edge(self, from_vertex: Graph.Vertex, to_vertex: Graph.Vertex, weight: float = 1.0) -> None:
        self.edges_by_source[from_vertex.key][to_vertex.key] = weight

    def get_edges_from_vertex(self, from_vertex: Graph.Vertex) -> Iterator[Tuple[Graph.Vertex, float]]:
        for key, weight in self.edges_by_source.get(from_vertex.key, {}).items():
            yield self.get_vertex(key), weight


class GraphAdjacencyMatrix[K, V](Graph):
    """
    Graph implemented with an adjacency matrix. All vertices must be added before any edge is added.
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

    def add_edge(self, from_vertex: Graph.Vertex, to_vertex: Graph.Vertex, weight: float = 1.0) -> None:
        if len(self.matrix) == 0:
            self.matrix = [None] * (len(self.vertices) ** 2)
        self.matrix[self.get_edge_index(from_vertex, to_vertex)] = weight

    def get_edge_index(self, from_vertex: Graph.Vertex, to_vertex: Graph.Vertex) -> int:
        return from_vertex.index * len(self.vertices) + to_vertex.index

    def get_edge_weight(self, from_vertex: Graph.Vertex, to_vertex: Graph.Vertex) -> Optional[float]:
        if len(self.matrix) > 0:
            return self.matrix[self.get_edge_index(from_vertex, to_vertex)]
        else:
            # special case for no edges added
            return None

    def get_edges_from_vertex(self, from_vertex: Graph.Vertex) -> Iterator[Tuple[Graph.Vertex, float]]:
        if len(self.matrix) > 0:
            for vertex in self.vertices.values():
                weight = self.get_edge_weight(from_vertex, vertex)
                if weight is not None:
                    yield vertex, weight
