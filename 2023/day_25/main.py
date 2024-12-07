import os
from operator import add, mul
import itertools
import math
from tqdm import tqdm
import sys

# Increase recursion depth limit
sys.setrecursionlimit(10000)

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    items = [line.split(':') for line in lines]
    return {item[0]: [it for it in item[1].strip().split(" ")] for item in items}

class Graph:
    def __init__(self, gdict=None):
        # Dictionary to store adjacency list
        self.adjacency_list = {}
        if gdict is not None:
            self.add_graph_from_dict(gdict)

    def add_graph_from_dict(self, gdict):
        for node, neighbours in gdict.items():
            if node not in self.adjacency_list:
                self.add_node(node)
            for neighbour in neighbours:
                if neighbour not in self.adjacency_list:
                    self.add_node(neighbour)
                self.add_edge(node, neighbour)

    def add_node(self, node):
        # Add a node to the graph
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, node1, node2):
        # Add an edge between two nodes
        if node1 not in self.adjacency_list:
            self.add_node(node1)
        if node2 not in self.adjacency_list:
            self.add_node(node2)
        if node2 not in self.adjacency_list[node1]:
            self.adjacency_list[node1].append(node2)
        if node1 not in self.adjacency_list[node2]:
            self.adjacency_list[node2].append(node1)  # For undirected graph

    def remove_edge(self, node1, node2):
        if (node1 in self.adjacency_list) and (node2 in self.adjacency_list):
            self.adjacency_list[node1].remove(node2)
            self.adjacency_list[node2].remove(node1)

    def get_nodes(self):
        # Return a list of all nodes
        return list(self.adjacency_list.keys())

    def get_number_of_connections(self, node):
        # Return the number of connections for a node
        if node in self.adjacency_list:
            return len(self.adjacency_list[node])
        return 0

    def get_edges(self):
        # Return all edges as a list of tuples
        edges = []
        for node, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                if (neighbor, node) not in edges:  # Avoid duplicates for undirected graph
                    edges.append((node, neighbor))
        return edges

    def get_connected_nodes(self, node):
        # Return nodes connected to a specific node
        if node in self.adjacency_list:
            return self.adjacency_list[node]
        return []
    
    def node_connections_count(self):
        ccount = {}
        for node in list(self.adjacency_list.keys()):
            ccount[node] = self.get_number_of_connections(node)
        return ccount

    def edge_connections_count(self):
        ccount = {}
        edges = self.get_edges()
        for edge in edges:
            ccount[edge] = self.get_number_of_connections(edge[0]) + self.get_number_of_connections(edge[1])
        return ccount

    def display(self):
        return self.adjacency_list
    
    def _dfs(self, node, visited):
        visited[node] = True
        size = 1
        for neighbor in self.adjacency_list[node]:
            if not visited[neighbor]:
                size += self._dfs(neighbor, visited)
        return size

    def count_components(self):
        nodes = self.get_nodes()
        visited = {node: False for node in nodes}  # Track visited nodes
        component_count = 0
        sizes = []
        
        # Loop through all nodes in the graph
        for node in nodes:
            if not visited[node]:  # If the node is not visited, it's a new component
                size = self._dfs(node, visited)  # Perform DFS from this node
                component_count += 1
                sizes.append(size)
        
        return component_count, sizes

def basic(graph):
    gdict = graph.display()
    data = graph.edge_connections_count()
    edges_sorted = sorted(data, key=data.get, reverse=True)

    #for i in range(len(edges_sorted)):
    for i in tqdm(range(len(edges_sorted)), desc="Looping through combinations of edges", unit="combinations"):    
        for j in tqdm(range(i+1, len(edges_sorted)), desc="Looping through combinations of edges", unit="combinations"):
            for k in tqdm(range(j+1, len(edges_sorted)), desc="Looping through combinations of edges", unit="combinations"):
                graph_t = Graph(gdict)
                graph_t.remove_edge(edges_sorted[i][0], edges_sorted[i][1])
                graph_t.remove_edge(edges_sorted[j][0], edges_sorted[j][1])
                graph_t.remove_edge(edges_sorted[k][0], edges_sorted[k][1])
                count, sizes = graph_t.count_components()
                if count > 1:
                    return sizes

def greedy(graph):
    gdict = graph.display()
    data = graph.edge_connections_count()
    edge_combinations = itertools.combinations(data.keys(), 3)
    edge_combinations_dict = {comb: sum(data[k] for k in comb) for comb in edge_combinations}
    edge_combinations_sorted = sorted(edge_combinations_dict, key=edge_combinations_dict.get, reverse=True)

    #for comb in tqdm(edge_combinations_sorted, desc="Looping through combinations of edges", unit="combinations"):
    for comb in edge_combinations_sorted:
        #print(comb)
        graph_t = Graph(gdict)
        for edge in comb:
            graph_t.remove_edge(edge[0], edge[1])
        count, sizes = graph_t.count_components()
        if count > 1:
            return sizes


def main(path=_path + "/input.txt", print_value=True):
    input = read(path)

    graph = Graph(input)
    #import timeit
    #print(timeit.timeit(lambda: basic(graph), number=1))
    #print(timeit.timeit(lambda: greedy(graph), number=1))
    sizes = basic(graph)
    #sizes = greedy(graph)
    res = math.prod(sizes)

    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    input = read(path)
    res = 0

    if print_value:
        print(res)
    return res

def check_example(func, input_filename = "example_input.txt", answer_filename = "example_answer.txt"):
    example_calculation = func(_path + "/" + input_filename, print_value=False)
    with open(_path + "/" + answer_filename, "r") as input_data_file:
        example_answer = int(input_data_file.read())
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

if __name__ == "__main__":
    #check_example(main, input_filename = "example_input.txt", answer_filename = "example_answer.txt")

    #run on the input
    main()

    # check_example(main2, input_filename = "example_input.txt", answer_filename = "example_answer_2.txt")

    # # run on the input
    # main_2()
