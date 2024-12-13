import os
import numpy as np

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    items = [[char for char in line] for line in lines]
    return items       

def is_valid(i, j, height, width):
    return ((i >=0) and (i < height) and (j >= 0) and (j < width))

def get_neighbours(data, v, i_coord, j_coord):
    height = len(data)
    width = len(data[0])
    neighbours = []
    for i,j in [(i_coord+1, j_coord), (i_coord, j_coord+1), (i_coord-1, j_coord), (i_coord, j_coord-1)]:
        if is_valid(i, j, height, width) and (data[i][j] == v):
            neighbours.append((i,j))
    return neighbours



def combine_stats(data, plants_dict):
    for i, line in enumerate(data):
        for j, v in enumerate(line):
            plants_dict.setdefault(v, {})[(i,j)] = get_neighbours(data, v, i, j)

def search_neighbours(v, coord, plants_dict, garden, plant_coord_list):
    if coord in garden:
        return
    else:
        garden.append(coord)
        plant_coord_list.remove(coord)
        neighbours = plants_dict[v][coord]
        for neighbour in neighbours:
            search_neighbours(v, neighbour, plants_dict, garden, plant_coord_list)



def get_gardens(data, plants_dict):
    plant_coord_list = [(i,j) for i, line in enumerate(data) for j, _ in enumerate(line)]
    gardens = []
    #for coord in plant_coord_list:
    while len(plant_coord_list) > 0:
        coord = plant_coord_list[0]
        garden = []
        v = data[coord[0]][coord[1]]
        search_neighbours(v, coord, plants_dict, garden, plant_coord_list)
        gardens.append(garden)
    return gardens

def garden_perimeter(data, garden, plants_dict):
    per = 0
    for coord in garden:
        v = data[coord[0]][coord[1]]
        per += 4 - len(plants_dict[v][coord])
    return per

def garden_area(garden):
    return len(garden)

def main(path=_path + "/input.txt", print_value=True):
    input = read(path)
    plants_dict = {}
    combine_stats(input, plants_dict)
    gardens = get_gardens(input, plants_dict)

    res = 0
    for garden in gardens:
        perimeter = garden_perimeter(input, garden, plants_dict)
        area = garden_area(garden)
        res += area*perimeter

    if print_value:
        print(res)
    return res


def edge_counter(gardens, plants_dict, data, order):
    edges = {}
    for g, garden in enumerate(gardens):
        edges[g] = {}
        for c1, c2 in garden:
            edges[g][(c1,c2)] = []
            v = data[c1][c2]
            neighbours = plants_dict[v][(c1,c2)]
            for k, (i, j) in enumerate(order):
                if (c1+i, c2+j) not in neighbours:
                    edges[g][(c1,c2)].append(k)
    return edges

def get_possible_edge_neighbours(edge):

    dcoords = [(1,1), (0,1), (0,0), (1,-1), (0,-1), (0,0)]
    neighbour_edge_n = [3, 0, 1, 1, 0, 3]
    rotation_matrix = np.array([[0, -1],
                                [1,  0]])
    for _ in range(edge):
        for i, dcoord in enumerate(dcoords):
            dcoords[i] = np.dot(rotation_matrix, dcoord)
    neighbour_edge_n = [(ed + edge)%4 for ed in neighbour_edge_n]
    return dcoords, neighbour_edge_n
    

def get_edge_neighbours(edge, coord, valid_edge_coords, edges_g):
    neighbour_edges = []
    dcoords, neighbour_edge_n = get_possible_edge_neighbours(edge)
    for (di, dj), en in zip(dcoords, neighbour_edge_n):
        neighbour_coord = (coord[0] + di, coord[1] + dj)
        if (neighbour_coord in valid_edge_coords) and (en in edges_g[neighbour_coord]):
            neighbour_edges.append((neighbour_coord[0], neighbour_coord[1], en))
    return neighbour_edges

def edge_neighbours(gardens, edges):
    neighbour_edge_dict = {}
    for g, garden in enumerate(gardens):
        neighbour_edge_dict[g] = {}
        valid_edge_coords = list(edges[g].keys())
        for coord, c_edges in edges[g].items():
            for edge in c_edges:
                neighbour_edges = get_edge_neighbours(edge, coord, valid_edge_coords, edges[g])
                neighbour_edge_dict[g][coord[0], coord[1], edge] = neighbour_edges
    return neighbour_edge_dict

def side_counter_new(edge_list, current_edge, neighbour_edge_dict_g, side_n, start_edge):
    for edge in neighbour_edge_dict_g[current_edge]:
        if edge in edge_list:
            if edge[2] != current_edge[2]:
                side_n += 1
            edge_list.remove(edge)
            side_n = side_counter_new(edge_list, edge, neighbour_edge_dict_g, side_n, start_edge)
            return side_n
    
    if start_edge[2] == current_edge[2]:
        side_n += -1
    return side_n

def count_sides_new(gardens, neighbour_edge_dict):
    sides = []
    for g, garden in enumerate(gardens):
        edge_list = list(neighbour_edge_dict[g].keys())
        side_sum = 0
        while len(edge_list) > 0:
            start_edge = edge_list[0]
            edge_list.remove(start_edge)
            side_n = 1
            side_n = side_counter_new(edge_list, start_edge, neighbour_edge_dict[g], side_n, start_edge)
            side_sum += side_n
        sides.append(side_sum)
    return sides
        

def main_2(path=_path + "/input.txt", print_value=True):
    """
    Incorrect solution.

    Need to go edge by edge, not plant by plant.

    Orientation of edges
    .2.
    3P1
    .0.

    if edge is 2 it can be connected to 6 other edges.
    Assume that coords of plant are i,j where i is vertical, j is horisontal (order of reading lines, sorry)
    6 options:
    1. edge 1 from node (i-1, j-1). Diagonal, not node neighbour.
    2. edge 2 from node (i, j-1). Neighbour. Doesn't increase the side count
    3. edge 3 of the same node (i,j). 
    4. edge 3 of the node (i-1, j+1). Diagonal, not node neighbour.
    5. edge 2 from node (i, j+1). Neighbour. Doesn't increase the side count
    6. edge 1 of the same node (i,j). 

    neigbour is valid if it is in the edge list for the garden
    
    need to create dictionary with edge neighbours based on 3 coords: 2 coords of the node and coord of the edge

    If edge-neighbour has the same edge number then side count does not increase, otherwise it does.

    Need to create a list of edges as a 3 coordinate form for every garden. 
    Start at some edge and move through neighbours. 
    At every step delete edges from the edge list.
    Continue until the list is empty.
    """
    input = read(path)
    plants_dict = {}
    combine_stats(input, plants_dict)
    gardens = get_gardens(input, plants_dict)
    order = [(1,0), (0,1), (-1,0), (0,-1)]
    edges = edge_counter(gardens, plants_dict, input, order)

    neighbour_edge_dict = edge_neighbours(gardens, edges)
    sides =  count_sides_new(gardens, neighbour_edge_dict)

    res = 0
    for g, garden in enumerate(gardens):
        res += len(garden) * sides[g]
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
    check_example(main, input_filename = "example_input_2.txt", answer_filename = "example_answer_2.txt")
    check_example(main, input_filename = "example_input.txt", answer_filename = "example_answer.txt")

    # #run on the input
    main()
    check_example(main_2, input_filename = "example_input_3.txt", answer_filename = "example_answer_3.txt")
    check_example(main_2, input_filename = "example_input_4.txt", answer_filename = "example_answer_4.txt")
    check_example(main_2, input_filename = "example_input_5.txt", answer_filename = "example_answer_5.txt")
    check_example(main_2, input_filename = "example_input.txt", answer_filename = "example_answer_6.txt")

    # #run on the input
    main_2()