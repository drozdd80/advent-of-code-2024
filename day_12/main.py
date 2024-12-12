import os

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

def diagonal_neighbour_case(plant,plants_coord_dict, garden_left, edges_n, edges_g, start, height, width):
    plant_neighbours = plants_coord_dict[plant]
    last_node = plant
    for i, j in [(1,1), (1,-1), (-1,-1), (-1,1)]:
        ic = plant[0] + i
        jc = plant[1] + j
        current = (ic, jc)
        if is_valid(ic, jc, height, width):
            current_neighbours = plants_coord_dict[current]
            neighbour_overlap = len([i for i in current_neighbours if i in plant_neighbours])
            if (current in garden_left) and (neighbour_overlap > 0):
                garden_left.remove(current)
                uncommon_edges = [i for i in edges_g[current] if i not in edges_g[plant]]
                edges_n += len(edges_g[current])
                edges_n, last_node = side_counter(edges_g, plants_coord_dict, current, garden_left, edges_n, start, height, width, uncommon_edges)
                return edges_n, last_node
    return edges_n, last_node

def side_counter(edges_g, plants_coord_dict, plant, garden_left, edges_n, start, height, width, uncommon_edges):
    plant_edges = edges_g[plant]
    if len(garden_left) == 0:
        if (len(edges_g[plant]) == 4):
            return edges_n, plant
        else:

        #import ipdb; ipdb.set_trace()
            start_edges = edges_g[start]
            common_edges = [i for i in start_edges if i in uncommon_edges]
            for edge in common_edges:
                if (edge == 0) or (edge == 2):
                    if start[0] == plant[0]:
                        edges_n += -1
                if (edge == 1) or (edge == 3):
                    if start[1] == plant[1]:
                        edges_n += -1
                
            return edges_n, plant
    
    for neighbour in plants_coord_dict[plant]:
        neighbour_edges = edges_g[neighbour]
        if neighbour in garden_left:
            garden_left.remove(neighbour)
            common_edges = [i for i in neighbour_edges if i in plant_edges]
            uncommon_edges = [i for i in neighbour_edges if i not in plant_edges]
            #import ipdb; ipdb.set_trace()
            edges_n += len(neighbour_edges) - len(common_edges)
            edges_n, last_node = side_counter(edges_g, plants_coord_dict, neighbour, garden_left, edges_n, start, height, width, uncommon_edges)
            return edges_n, last_node
        
    edges_n, last_node = diagonal_neighbour_case(plant,plants_coord_dict, garden_left, edges_n, edges_g, start, height, width)

    return edges_n, last_node



def count_sides(gardens, edges, plants_coord_dict, height, width):
    sides = []
    for g, garden in enumerate(gardens):
        # garden with edges
        edge_garden = list(edges[g].keys())
        start = edge_garden[0]
        edge_garden.remove(start)
        edges_n = len(edges[g][start])
        edges_n, last_node = side_counter(edges_g=edges[g], plants_coord_dict=plants_coord_dict, plant=start, garden_left=edge_garden, edges_n=edges_n, start=start, height=height, width=width, uncommon_edges=edges[g][start])
        
        # remove common edges of the start node
        # if last_node in plants_coord_dict[start]:
        #     common_edges = [i for i in edges[g][last_node] if i in edges[g][start]]
        #     edges_n += -len(common_edges)
        sides.append(edges_n)
            # check neightbours
            # count how many edges with the same side do they have in common
            # subtrack them
            # continue until you get to the original plant
            # if there are no new neighbours left except the last one, it means that the shape it concave
            # need to check plants at diagonals (i+1, j+1). But they need to have a common neighbour.
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

    need to create dictionary with edge neighbours based on 3 coords: 2 coords of the node and coord of the edge

    If edge-neighbour has the same edge number then side count does not increase, otherwise it does.

    Need to create a list of edges as a 3 coordinate form for every garden. 
    Start at some edge and move through neighbours. 
    At every step delete edges from the edge list.
    Continue until the list is empty.
    """
    input = read(path)
    height = len(input)
    width = len(input[0])
    plants_dict = {}
    combine_stats(input, plants_dict)
    gardens = get_gardens(input, plants_dict)
    order = [(1,0), (0,1), (-1,0), (0,-1)]
    edges = edge_counter(gardens, plants_dict, input, order)
    plants_coord_dict = {k:v for val in plants_dict.values() for k,v in val.items()}
    sides = count_sides(gardens, edges, plants_coord_dict, height, width)

    res = 0
    for g, garden in enumerate(gardens):
        res += len(garden) * sides[g]
    #import ipdb; ipdb.set_trace()
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
    # check_example(main, input_filename = "example_input_2.txt", answer_filename = "example_answer_2.txt")
    # check_example(main, input_filename = "example_input.txt", answer_filename = "example_answer.txt")

    # # #run on the input
    # main()
    #main(path=_path + "/example_custom_input_1.txt")
    main_2(path=_path + "/example_custom_input_1.txt")
    #check_example(main_2, input_filename = "example_input_3.txt", answer_filename = "example_answer_3.txt")
    # check_example(main_2, input_filename = "example_input_4.txt", answer_filename = "example_answer_4.txt")
    # check_example(main_2, input_filename = "example_input_5.txt", answer_filename = "example_answer_5.txt")
    # check_example(main_2, input_filename = "example_input.txt", answer_filename = "example_answer_6.txt")

    # #run on the input
    # main_2()