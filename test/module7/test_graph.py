import pytest

from module7.graph import Graph, GraphAdjacencyList, GraphAdjacencyMatrix


@pytest.fixture(params=[GraphAdjacencyList, GraphAdjacencyMatrix])
def graph(request) -> Graph:
    # Instantiate the queue implementation and use it build a message queue simulator
    return request.param()


def test_empty(graph):
    assert len(graph.vertices) == 0
    assert list(graph.traverse_depth_first()) == []

    assert "" not in graph


def test_add_vertex(graph):
    vertex1 = graph.add_vertex(1, "a")
    vertex2 = graph.add_vertex(2, "b")
    vertex3 = graph.add_vertex(3, "c")

    assert graph.vertices == {1: vertex1, 2: vertex2, 3: vertex3}
    assert list(graph.get_edges_from_vertex(vertex1)) == []
    assert list(graph.get_edges_from_vertex(vertex2)) == []
    assert list(graph.get_edges_from_vertex(vertex3)) == []

    assert 1 in graph
    assert 2 in graph
    assert 3 in graph
    assert 0 not in graph


def test_add_vertex_duplicate_key(graph):
    graph.add_vertex(1, "a")
    with pytest.raises(KeyError):
        graph.add_vertex(1, "b")


def test_add_edge(graph):
    vertex1 = graph.add_vertex(1, "a")
    vertex2 = graph.add_vertex(2, "b")
    vertex3 = graph.add_vertex(3, "c")

    graph.add_edge(vertex1, vertex2)
    graph.add_edge(vertex1, vertex3)
    graph.add_edge(vertex2, vertex3)

    assert graph.get_edge_weight(vertex1, vertex2) == 1.0
    assert graph.get_edge_weight(vertex1, vertex3) == 1.0
    assert graph.get_edge_weight(vertex2, vertex3) == 1.0
    assert graph.get_edge_weight(vertex2, vertex1) is None
    assert graph.get_edge_weight(vertex3, vertex1) is None
    assert graph.get_edge_weight(vertex3, vertex2) is None

    assert list(graph.get_edges_from_vertex(vertex1)) == [(vertex2, 1.0), (vertex3, 1.0)]
    assert list(graph.get_edges_from_vertex(vertex2)) == [(vertex3, 1.0)]
    assert list(graph.get_edges_from_vertex(vertex3)) == []

    assert graph.get_edge_weight(vertex1, vertex2) == 1.0


def test_add_edge_with_weight(graph):
    vertex1 = graph.add_vertex(1, "a")
    vertex2 = graph.add_vertex(2, "b")
    vertex3 = graph.add_vertex(3, "c")

    graph.add_edge(vertex1, vertex2, 2)
    graph.add_edge(vertex1, vertex3, 3)
    graph.add_edge(vertex2, vertex3, 4)

    assert graph.get_edge_weight(vertex1, vertex2) == 2.0
    assert graph.get_edge_weight(vertex1, vertex3) == 3.0
    assert graph.get_edge_weight(vertex2, vertex3) == 4.0

    assert graph.get_edge_weight(vertex2, vertex1) is None
    assert graph.get_edge_weight(vertex3, vertex1) is None
    assert graph.get_edge_weight(vertex3, vertex2) is None

    assert list(graph.get_edges_from_vertex(vertex1)) == [(vertex2, 2.0), (vertex3, 3.0)]
    assert list(graph.get_edges_from_vertex(vertex2)) == [(vertex3, 4.0)]
    assert list(graph.get_edges_from_vertex(vertex3)) == []


def test_add_edge_undirected(graph):
    vertex1 = graph.add_vertex(1, "a")
    vertex2 = graph.add_vertex(2, "b")
    vertex3 = graph.add_vertex(3, "c")

    graph.add_edge_undirected(vertex1, vertex2)
    graph.add_edge_undirected(vertex1, vertex3)
    graph.add_edge_undirected(vertex2, vertex3)

    assert graph.get_edge_weight(vertex1, vertex2) == 1.0
    assert graph.get_edge_weight(vertex1, vertex3) == 1.0
    assert graph.get_edge_weight(vertex2, vertex3) == 1.0
    assert graph.get_edge_weight(vertex2, vertex1) == 1.0
    assert graph.get_edge_weight(vertex3, vertex1) == 1.0
    assert graph.get_edge_weight(vertex3, vertex2) == 1.0

    assert list(graph.get_edges_from_vertex(vertex1)) == [(vertex2, 1.0), (vertex3, 1.0)]
    assert list(graph.get_edges_from_vertex(vertex2)) == [(vertex1, 1.0), (vertex3, 1.0)]
    assert list(graph.get_edges_from_vertex(vertex3)) == [(vertex1, 1.0), (vertex2, 1.0)]


def test_add_edge_undirected_with_weight(graph):
    vertex1 = graph.add_vertex(1, "a")
    vertex2 = graph.add_vertex(2, "b")
    vertex3 = graph.add_vertex(3, "c")

    graph.add_edge_undirected(vertex1, vertex2, 2.0)
    graph.add_edge_undirected(vertex1, vertex3, 3.0)
    graph.add_edge_undirected(vertex2, vertex3, 4.0)

    assert graph.get_edge_weight(vertex1, vertex2) == 2.0
    assert graph.get_edge_weight(vertex1, vertex3) == 3.0
    assert graph.get_edge_weight(vertex2, vertex3) == 4.0
    assert graph.get_edge_weight(vertex2, vertex1) == 2.0
    assert graph.get_edge_weight(vertex3, vertex1) == 3.0
    assert graph.get_edge_weight(vertex3, vertex2) == 4.0

    assert list(graph.get_edges_from_vertex(vertex1)) == [(vertex2, 2.0), (vertex3, 3.0)]
    assert list(graph.get_edges_from_vertex(vertex2)) == [(vertex1, 2.0), (vertex3, 4.0)]
    assert list(graph.get_edges_from_vertex(vertex3)) == [(vertex1, 3.0), (vertex2, 4.0)]


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
