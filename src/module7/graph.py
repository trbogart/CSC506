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

        def __repr__(self):
            return f'Vertex(key: {repr(self.key)}, index: {self.index}, value: {repr(self.value)})'

    def __init__(self):
        self.vertices = dict[K, Graph.Vertex]()  # key -> vertex

    def __repr__(self):
        def get_edges_string(vertex):
            for target_vertex, weight in self.get_edges_from_vertex(vertex):
                yield f'{repr(target_vertex.key)}: {weight}'

        def get_vertex_string(vertex):
            return f'{repr(vertex.value)}: {{{', '.join(get_edges_string(vertex))}}}'

        vertices = ', '.join([get_vertex_string(vertex) for vertex in self.vertices.values()])

        return f'{{{vertices}}}'

    def add_vertex(self, key: K, data: V = None) -> Vertex:
        """
        Adds a new vertex to the graph.
        :param key: key to add
        :param data: data to add
        :return: the vertex that was added
        :raises KeyError: if vertex with given key already exists
        """
        if key in self.vertices.keys():
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
        Adds a new undirected edge to the graph.
        :param vertex1: first vertex
        :param vertex2: second vertex
        :param weight: weight of the edge (1 by default)
        """
        self.add_edge(vertex1, vertex2, weight)
        self.add_edge(vertex2, vertex1, weight)

    @abstractmethod
    def edges_ordered(self) -> bool:
        """
        Returns true if edges are ordered.
        Used for testing.
        """
        pass

    @abstractmethod
    def add_edge(self, source_vertex: Vertex, dest_vertex: Vertex, weight: float = 1.0) -> None:
        """
        Adds a new directed edge to the graph.
        :param source_vertex: source vertex
        :param dest_vertex: destination vertex
        :param weight: weight of the edge (1 by default)
        """
        pass

    @abstractmethod
    def get_edge_weight(self, source_vertex: Vertex, dest_vertex: Vertex) -> Optional[float]:
        """
        Returns the weight of the edge between two vertices, or None if there is no edge.
        :param source_vertex: source vertex
        :param dest_vertex: destination vertex
        :return: weight of the edge, or None if there is no edge
        """
        pass

    @abstractmethod
    def get_edges_from_vertex(self, source_vertex: Vertex) -> Iterator[Tuple[Vertex, float]]:
        """
        Returns an iterator over all destination vertices and weights from the given vertex.
        Order depends on implementation.
        :param source_vertex: source vertex
        :return: an iterator, which may be empty, over all destination vertices and weights from this vertex
        """
        pass

    def traverse_depth_first(self, root_vertex: Optional[Vertex] = None) -> Iterator[Vertex]:
        """
        Do a depth-first traversal.
        :param root_vertex: root vertex, or None to traverse all vertices.
        :return: depth-first iterator over vertices
        """
        visited = set[self.Vertex]()
        if root_vertex is None:
            # iterate all vertices
            for vertex in self.vertices.values():
                yield from self._traverse_depth_first(vertex, visited)
        else:
            # iterate given vertex only
            yield from self._traverse_depth_first(root_vertex, visited)

    def _traverse_depth_first(self, current_vertex: Vertex, visited: set[Vertex]) -> Iterator[Vertex]:
        """
        Internal method to do a depth-first traversal of subgraph for given vertex.
        :param current_vertex: vertex to traverse
        :param visited: vertices that have already been visited
        :return: depth-first iterator over vertices
        """
        if current_vertex not in visited:
            visited.add(current_vertex)
            for dest_vertex, _ in self.get_edges_from_vertex(current_vertex):
                yield from self._traverse_depth_first(dest_vertex, visited)
            yield current_vertex

    def traverse_breadth_first(self, root_vertex: Vertex) -> Iterator[Vertex]:
        """
        Do a breadth-first traversal of all vertices.
        :param root_vertex: root vertex.
        :return: breadth-first iterator over vertices
        """
        discovered = {root_vertex}
        queue = deque[Graph.Vertex]()
        queue.append(root_vertex)
        while len(queue) > 0:
            current_vertex = queue.popleft()
            yield current_vertex
            for dest_vertex, _ in self.get_edges_from_vertex(current_vertex):
                if dest_vertex not in discovered:
                    discovered.add(dest_vertex)
                    queue.append(dest_vertex)

    def shortest_path(self, start_vertex: Vertex, end_vertex: Vertex) -> list[Vertex]:
        """
        Returns the shortest path between two vertices, or an empty list if there is no path.
        Will not work if there are negative weight cycles.
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
