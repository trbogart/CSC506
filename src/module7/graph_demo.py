from module7.graph import Graph


class GraphDemo:
    def __init__(self, description: str, graph: Graph):
        print(f'Demo for {description} graph')
        print(f'See also unit tests: test_graph.py')
        print()
        self.graph = self

        # setup graph
        #             |v2|<-------5--------|v4|
        #             |  |                 |  |
        # |v1|---2--->|  |--------1------->|  |<---3---|v5|----+
        # |  |        |  |                 |  |        |  |    |
        # |  |        |  |---1-->|v3|--1-->|  |----1-->|  |<-1-+
        # |  |                   |  |                  |  |
        # |  |---------4-------->|  |---------4------->|  |
        # |  |                                         |  |
        # |  |---------------------1------------------>|  |

        v1 = graph.add_vertex('v1')
        v2 = graph.add_vertex('v2')
        v3 = graph.add_vertex('v3')
        v4 = graph.add_vertex('v4')
        v5 = graph.add_vertex('v5')

        graph.add_edge(v1, v2, 2)
        graph.add_edge(v1, v3, 4)
        graph.add_edge(v1, v5)
        graph.add_edge(v2, v3)
        graph.add_edge(v2, v4)
        graph.add_edge(v3, v4)
        graph.add_edge(v3, v5, 4)
        graph.add_edge(v4, v2, 5)
        graph.add_edge(v4, v5)
        graph.add_edge(v5, v4, 3)

        print(f'Graph: {graph}')
        print()
        print('Depth-first traversal')
        for vertex in graph.traverse_depth_first(v1):
            print(f'- Vertex: {vertex.key}')

        print()
        print('Breadth-first traversal')
        for vertex in graph.traverse_breadth_first(v1):
            print(f'- Vertex: {vertex.key}')

        print_shortest_path(graph, v1, v3, '(v1->v3 is longer)')
        print_shortest_path(graph, v2, v4)
        print_shortest_path(graph, v3, v1)  # no path
        print_shortest_path(graph, v4, v3)
        print_shortest_path(graph, v5, v3)


def print_shortest_path(graph, start_vertex, end_vertex, suffix=''):
    print()
    print(f'Shortest path between {start_vertex.key} and {end_vertex.key} {suffix}')
    shortest_path = graph.shortest_path(start_vertex, end_vertex)
    if len(shortest_path) == 0:
        print('- No path')
    else:
        total_distance = 0
        prev_vertex = shortest_path[0]
        for next_vertex in shortest_path[1:]:
            distance = graph.get_edge_weight(prev_vertex, next_vertex)
            print(f'- {prev_vertex.key} -> {next_vertex.key} ({distance})')
            prev_vertex = next_vertex
            total_distance += distance
        print(f'Total distance: {total_distance}')
