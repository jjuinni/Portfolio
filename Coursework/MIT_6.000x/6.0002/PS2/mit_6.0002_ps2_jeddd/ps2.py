# 6.0002 Problem Set 5
# Graph optimization
# Name: Jed

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: ①图中的节点表示学校里面的各个地点（楼房，building），用编号或名称表示。
#         ②节点之间的边代表从起点到终点的有向路径。
#         ③每条路径有两个属性，分别是总距离和室外距离。所有节点和有向边的集合构成
#        一张有向图。


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    print("Loading map from file...")
    graph = Digraph()  # 创建空图
    with open(map_filename) as file:
        for line in file:
            elements = line.split()  # 按空格分割成list
            src = Node(elements[0])
            dest = Node(elements[1])
            total_distance = int(elements[2])    # 数字类型
            outdoor_distance = int(elements[3])  # 数字类型

            if not graph.has_node(src):
                graph.add_node(src)
            if not graph.has_node(dest):
                graph.add_node(dest)
            graph.add_edge(WeightedEdge(src, dest, total_distance, outdoor_distance))

    return graph

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
# print('*** Problem 2c BEGIN ***')
# test_graph = load_map('test_load_map.txt')
# print(test_graph)
# print('*** Problem 2c END ***')


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# 目标函数：要找到从起点到终点的最短路径（total_distance之和最小）
# 约束条件：室外路径总长度不超过给定限制（outdoor_distance之和不超过限制）


# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    start_node = Node(start)  # 转换为Node对象
    end_node = Node(end)      # 转换为Node对象
    if not digraph.has_node(start_node) or not digraph.has_node(end_node):
        raise ValueError('Node not exist')
    elif start == end:        # 递归到end时，直接返回当前路径及其总长度
        return path[0], path[1]
    else:
        for edge in digraph.edges[start_node]:
            # 加入下一个节点（当前起点的邻接点），构造出一个新路径，作为path参数进行递归
            next_node = edge.get_destination().get_name()
            next_path_nodes = path[0] + [next_node]    # 新路径经过的节点列表
            next_path_total_dist = path[1] + edge.get_total_distance()         # 新路径的总长度
            next_path_outdoor_dist = path[2] + edge.get_outdoor_distance()     # 新路径的室外长度
            next_path = [next_path_nodes, next_path_total_dist, next_path_outdoor_dist]  # 新的path参数

            if (next_node not in path[0]) and (next_path[2] <= max_dist_outdoors) and (next_path[1] < best_dist):
                # 递归
                new_best_path = get_best_path(digraph, next_node, end, next_path, max_dist_outdoors, best_dist, best_path)
                # 更新
                if new_best_path is not None and new_best_path[1] < best_dist:
                    best_dist = new_best_path[1]  # 新的最短路径的长度
                    best_path = new_best_path[0]  # 新的最短路径的节点列表

        if best_path: # 列表非空，返回元组
            return best_path, best_dist
        else:         # 列表为空，返回None
            return None


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    result = get_best_path(digraph, start, end, [[start], 0, 0], max_dist_outdoors, float('inf'), [])
    if result is None:
        raise ValueError('get_best_path returned None')
    best_path, best_dist = result
    if best_dist > max_total_dist:
        raise ValueError('No path can satisfies the constraints')
    else:
        return best_path

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()