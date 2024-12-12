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
    plant_coord_list = [(i,j) for j, line in enumerate(data) for i, _ in enumerate(line)]
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


def main_2(path=_path + "/input.txt", print_value=True):
    #input = read(path)

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
    check_example(main, input_filename = "example_input_2.txt", answer_filename = "example_answer_2.txt")
    check_example(main, input_filename = "example_input.txt", answer_filename = "example_answer.txt")

    # #run on the input
    main()

    # check_example(main_2, input_filename = "example_input.txt", answer_filename = "example_answer_2.txt")

    # #run on the input
    # main_2()