import pytest

from module7.graph import Graph, GraphAdjacencyList, GraphAdjacencyMatrix


@pytest.fixture(params=[GraphAdjacencyList, GraphAdjacencyMatrix])
def graph(request) -> Graph:
    # Instantiate the queue implementation and use it build a message queue simulator
    return request.param()


def test_empty(graph):
    assert len(graph.vertices) == 0
    assert list(graph.traverse_depth_first()) == []

    assert '' not in graph


def test_add_vertex(graph):
    vertex1 = graph.add_vertex(1, 'a')
    vertex2 = graph.add_vertex(2, 'b')
    vertex3 = graph.add_vertex(3, 'c')

    assert graph.vertices == {1: vertex1, 2: vertex2, 3: vertex3}
    assert list(graph.get_edges_from_vertex(vertex1)) == []
    assert list(graph.get_edges_from_vertex(vertex2)) == []
    assert list(graph.get_edges_from_vertex(vertex3)) == []

    assert 1 in graph
    assert 2 in graph
    assert 3 in graph
    assert 0 not in graph


def test_add_vertex_duplicate_key(graph):
    graph.add_vertex(1, 'a')
    with pytest.raises(KeyError):
        graph.add_vertex(1, 'b')


def test_add_edge(graph):
    vertex1 = graph.add_vertex(1, 'a')
    vertex2 = graph.add_vertex(2, 'b')
    vertex3 = graph.add_vertex(3, 'c')

    graph.add_edge(vertex1, vertex2)
    graph.add_edge(vertex1, vertex3)
    graph.add_edge(vertex2, vertex3)

    assert graph.get_edge_weight(vertex1, vertex2) == 1
    assert graph.get_edge_weight(vertex1, vertex3) == 1
    assert graph.get_edge_weight(vertex2, vertex3) == 1
    assert graph.get_edge_weight(vertex2, vertex1) is None
    assert graph.get_edge_weight(vertex3, vertex1) is None
    assert graph.get_edge_weight(vertex3, vertex2) is None

    assert list(graph.get_edges_from_vertex(vertex1)) == [(vertex2, 1), (vertex3, 1)]
    assert list(graph.get_edges_from_vertex(vertex2)) == [(vertex3, 1)]
    assert list(graph.get_edges_from_vertex(vertex3)) == []

    assert graph.get_edge_weight(vertex1, vertex2) == 1


def test_add_edge_with_weight(graph):
    vertex1 = graph.add_vertex(1, 'a')
    vertex2 = graph.add_vertex(2, 'b')
    vertex3 = graph.add_vertex(3, 'c')

    graph.add_edge(vertex1, vertex2, 2)
    graph.add_edge(vertex1, vertex3, 3)
    graph.add_edge(vertex2, vertex3, 4)

    assert graph.get_edge_weight(vertex1, vertex2) == 2
    assert graph.get_edge_weight(vertex1, vertex3) == 3
    assert graph.get_edge_weight(vertex2, vertex3) == 4

    assert graph.get_edge_weight(vertex2, vertex1) is None
    assert graph.get_edge_weight(vertex3, vertex1) is None
    assert graph.get_edge_weight(vertex3, vertex2) is None

    assert list(graph.get_edges_from_vertex(vertex1)) == [(vertex2, 2), (vertex3, 3)]
    assert list(graph.get_edges_from_vertex(vertex2)) == [(vertex3, 4)]
    assert list(graph.get_edges_from_vertex(vertex3)) == []


def test_add_edge_undirected(graph):
    vertex1 = graph.add_vertex(1, 'a')
    vertex2 = graph.add_vertex(2, 'b')
    vertex3 = graph.add_vertex(3, 'c')

    graph.add_edge_undirected(vertex1, vertex2)
    graph.add_edge_undirected(vertex1, vertex3)
    graph.add_edge_undirected(vertex2, vertex3)

    assert graph.get_edge_weight(vertex1, vertex2) == 1
    assert graph.get_edge_weight(vertex1, vertex3) == 1
    assert graph.get_edge_weight(vertex2, vertex3) == 1
    assert graph.get_edge_weight(vertex2, vertex1) == 1
    assert graph.get_edge_weight(vertex3, vertex1) == 1
    assert graph.get_edge_weight(vertex3, vertex2) == 1

    assert list(graph.get_edges_from_vertex(vertex1)) == [(vertex2, 1), (vertex3, 1)]
    assert list(graph.get_edges_from_vertex(vertex2)) == [(vertex1, 1), (vertex3, 1)]
    assert list(graph.get_edges_from_vertex(vertex3)) == [(vertex1, 1), (vertex2, 1)]


def test_add_edge_undirected_with_weight(graph):
    vertex1 = graph.add_vertex(1, 'a')
    vertex2 = graph.add_vertex(2, 'b')
    vertex3 = graph.add_vertex(3, 'c')

    graph.add_edge_undirected(vertex1, vertex2, 2)
    graph.add_edge_undirected(vertex1, vertex3, 3)
    graph.add_edge_undirected(vertex2, vertex3, 4)

    assert graph.get_edge_weight(vertex1, vertex2) == 2
    assert graph.get_edge_weight(vertex1, vertex3) == 3
    assert graph.get_edge_weight(vertex2, vertex3) == 4
    assert graph.get_edge_weight(vertex2, vertex1) == 2
    assert graph.get_edge_weight(vertex3, vertex1) == 3
    assert graph.get_edge_weight(vertex3, vertex2) == 4

    assert list(graph.get_edges_from_vertex(vertex1)) == [(vertex2, 2), (vertex3, 3)]
    assert list(graph.get_edges_from_vertex(vertex2)) == [(vertex1, 2), (vertex3, 4)]
    assert list(graph.get_edges_from_vertex(vertex3)) == [(vertex1, 3), (vertex2, 4)]


def test_depth_first_traversal_all(graph):
    vertex1 = graph.add_vertex(1)
    vertex2 = graph.add_vertex(2)
    vertex3 = graph.add_vertex(3)
    vertex4 = graph.add_vertex(4)
    vertex5 = graph.add_vertex(5)
    vertex6 = graph.add_vertex(6)

    graph.add_edge(vertex1, vertex2)
    graph.add_edge(vertex1, vertex3)
    graph.add_edge(vertex2, vertex3)
    graph.add_edge(vertex2, vertex4)
    graph.add_edge(vertex3, vertex5)

    vertices = list(graph.traverse_depth_first())
    assert set(vertices) == {vertex1, vertex2, vertex3, vertex4, vertex5, vertex6}
    assert vertices.index(vertex1) > vertices.index(vertex2)
    assert vertices.index(vertex1) > vertices.index(vertex3)
    assert vertices.index(vertex2) > vertices.index(vertex3)
    assert vertices.index(vertex2) > vertices.index(vertex4)
    assert vertices.index(vertex3) > vertices.index(vertex5)


def test_depth_first_traversal(graph):
    vertex1 = graph.add_vertex(1)
    vertex2 = graph.add_vertex(2)
    vertex3 = graph.add_vertex(3)
    vertex4 = graph.add_vertex(4)
    vertex5 = graph.add_vertex(5)
    _ = graph.add_vertex(6)  # ignored

    graph.add_edge(vertex1, vertex2)
    graph.add_edge(vertex1, vertex3)
    graph.add_edge(vertex2, vertex3)
    graph.add_edge(vertex2, vertex4)
    graph.add_edge(vertex3, vertex5)

    vertices = list(graph.traverse_depth_first(vertex1))
    assert set(vertices) == {vertex1, vertex2, vertex3, vertex4, vertex5}
    assert vertices.index(vertex1) > vertices.index(vertex2)
    assert vertices.index(vertex1) > vertices.index(vertex3)
    assert vertices.index(vertex2) > vertices.index(vertex3)
    assert vertices.index(vertex2) > vertices.index(vertex4)
    assert vertices.index(vertex3) > vertices.index(vertex5)


def test_breadth_first_traversal(graph):
    vertex1 = graph.add_vertex(1)
    vertex2 = graph.add_vertex(2)
    vertex3 = graph.add_vertex(3)
    vertex4 = graph.add_vertex(4)
    vertex5 = graph.add_vertex(5)
    _ = graph.add_vertex(6)  # ignored

    graph.add_edge(vertex1, vertex2)
    graph.add_edge(vertex1, vertex3)
    graph.add_edge(vertex2, vertex3)
    graph.add_edge(vertex2, vertex4)
    graph.add_edge(vertex3, vertex5)

    vertices = list(graph.traverse_breadth_first(vertex1))
    assert set(vertices) == {vertex1, vertex2, vertex3, vertex4, vertex5}
    assert vertices.index(vertex1) < vertices.index(vertex2)
    assert vertices.index(vertex1) < vertices.index(vertex3)
    assert vertices.index(vertex2) < vertices.index(vertex3)
    assert vertices.index(vertex2) < vertices.index(vertex4)
    assert vertices.index(vertex3) < vertices.index(vertex5)


def test_shortest_path(graph):
    vertex1 = graph.add_vertex(1)
    vertex2 = graph.add_vertex(2)
    vertex3 = graph.add_vertex(3)
    vertex4 = graph.add_vertex(4)
    vertex5 = graph.add_vertex(5)

    graph.add_edge(vertex1, vertex2, 2)
    graph.add_edge(vertex1, vertex3, 4)
    graph.add_edge(vertex1, vertex5)
    graph.add_edge(vertex2, vertex3)
    graph.add_edge(vertex2, vertex4)
    graph.add_edge(vertex3, vertex4)
    graph.add_edge(vertex3, vertex5, 4)
    graph.add_edge(vertex4, vertex2, 5)
    graph.add_edge(vertex4, vertex5)
    graph.add_edge(vertex5, vertex4, 5)

    def get_distance(path):
        distance = 0
        vertex = path[0]
        for i in range(1, len(path)):
            weight = graph.get_edge_weight(vertex, path[i])
            assert weight is not None
            distance += weight
            vertex = path[i]
        return distance

    def validate_shortest_path(start, end, expected_distance, *expected_path):
        path = graph.shortest_path(start, end)
        assert path == list(expected_path)
        if expected_distance is not None:
            assert get_distance(path) == expected_distance

    validate_shortest_path(vertex1, vertex2, 2, vertex1, vertex2)
    validate_shortest_path(vertex1, vertex3, 3, vertex1, vertex2, vertex3)
    validate_shortest_path(vertex1, vertex4, 3, vertex1, vertex2, vertex4)
    validate_shortest_path(vertex1, vertex5, 1, vertex1, vertex5)
    validate_shortest_path(vertex2, vertex1, None)
    validate_shortest_path(vertex2, vertex3, 1, vertex2, vertex3)
    validate_shortest_path(vertex2, vertex4, 1, vertex2, vertex4)
    validate_shortest_path(vertex2, vertex5, 2, vertex2, vertex4, vertex5)
    validate_shortest_path(vertex3, vertex1, None)
    validate_shortest_path(vertex3, vertex2, 6, vertex3, vertex4, vertex2)
    validate_shortest_path(vertex3, vertex4, 1, vertex3, vertex4)
    validate_shortest_path(vertex3, vertex5, 2, vertex3, vertex4, vertex5)
    validate_shortest_path(vertex4, vertex1, None)
    validate_shortest_path(vertex4, vertex2, 5, vertex4, vertex2)
    validate_shortest_path(vertex4, vertex3, 6, vertex4, vertex2, vertex3)
    validate_shortest_path(vertex4, vertex5, 1, vertex4, vertex5)
    validate_shortest_path(vertex5, vertex1, None)
    validate_shortest_path(vertex5, vertex2, 10, vertex5, vertex4, vertex2)
    validate_shortest_path(vertex5, vertex3, 11, vertex5, vertex4, vertex2, vertex3)
    validate_shortest_path(vertex5, vertex4, 5, vertex5, vertex4)

def test_repr(graph):
    vertex1 = graph.add_vertex('v1')
    vertex2 = graph.add_vertex('v2')
    vertex3 = graph.add_vertex('v3')
    graph.add_vertex('v4')

    graph.add_edge(vertex1, vertex2)
    graph.add_edge(vertex1, vertex3, 2)
    graph.add_edge(vertex2, vertex3, 3)
    graph.add_edge(vertex3, vertex1, 2)

    assert repr(graph) == "{'v1': {'v2': 1, 'v3': 2}, 'v2': {'v3': 3}, 'v3': {'v1': 2}, 'v4': {}}"