import pytest
from graph import Graph

EXAMPLE_INPUT = '''
    5, 9
    AB5, BC4, CD8, DC8, DE6
    AD5, CE2, EB3, AE7
'''

@pytest.fixture
def example_graph():
    return Graph.from_string(EXAMPLE_INPUT)


def test_from_string(example_graph):
    assert {'A', 'B', 'C', 'D', 'E'} == example_graph.nodes
    assert 5 == example_graph.distance(['A', 'B'])
    assert None == example_graph.distance(['A', 'C'])


def test_all_paths_max_depth(example_graph):
    one_stop = set(example_graph.all_paths_from('A', max_depth=1))
    assert {('A', 'B'), ('A', 'D'), ('A', 'E')} == one_stop


def test_all_paths_max_distance(example_graph):
    short_route = set(example_graph.all_paths_from('A', max_distance=10))
    assert {('A', 'B'), ('A', 'B', 'C'), ('A', 'E'), ('A', 'E', 'B'), ('A', 'D')} == short_route


@pytest.mark.parametrize(['route', 'expected_result'], (
    ['A-B-C', 9],
    ['A-D', 5],
    ['A-D-C', 13],
    ['A-E-B-C-D', 22],
    ['A-E-D', None],
))
def test_examples_1_through_5(example_graph, route, expected_result):
    node_path = route.split('-')
    assert expected_result == example_graph.distance(node_path)


def test_example_6(example_graph):  # all paths from C to C with <= 3 stops
    paths_from_c_to_c = {path for path in example_graph.all_paths_from('C', max_depth=3) if path[-1] == 'C'}
    assert 2 == len(paths_from_c_to_c)


def test_example_7(example_graph):  # all path from A to C with exactly 4 stops
    paths_from_a_to_c = {path for path in example_graph.all_paths_from('A', max_depth=4)
                              if path[-1] == 'C' and len(path) == 5}
    assert 3 == len(paths_from_a_to_c)


@pytest.mark.parametrize(['source_node', 'target_node', 'expected_distance'], (
    ['A', 'C', 9],  # distance travelled on shortest path from source to target
    ['B', 'B', 9],
))
def test_examples_8_and_9(example_graph, source_node, target_node, expected_distance):
    assert expected_distance == example_graph.shortest_distance(source_node, target_node)


def test_example_10(example_graph):  # all paths from C to C wtih distance < 30
    paths_from_c_to_c = {path for path in example_graph.all_paths_from('C', max_distance=29) if path[-1] == 'C'}
    assert 7 == len(paths_from_c_to_c)
