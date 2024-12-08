import os
from operator import add, mul
import itertools

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    items = [[char for char in line] for line in lines]
    return items        


def main(path=_path + "/input.txt", print_value=True):
    input = read(path)

    height = len(input)
    width = len(input[0])

    ant_pos = {}
    for i in range(height):
        for j in range(width):
            value = input[i][j]
            if value != '.':
                ant_pos.setdefault(value, []).append((i,j))

    antinodes = [[0 for _ in range(width)] for _ in range(height)]

    for key in ant_pos.keys():
        combs = itertools.combinations(ant_pos[key], 2)
        for comb in combs:
            for num, pos in enumerate(comb):
                k = 1
                i = pos[0] + k*(comb[1][0] - comb[0][0])*((-1)**(num+1))
                j = pos[1] + k*(comb[1][1] - comb[0][1])*((-1)**(num+1))

                if (i >= 0) and (i < height) and (j >= 0) and (j < width):
                    antinodes[i][j] = 1

    res = sum([sum(i) for i in antinodes])

    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    input = read(path)

    height = len(input)
    width = len(input[0])

    ant_pos = {}
    for i in range(height):
        for j in range(width):
            value = input[i][j]
            if value != '.':
                ant_pos.setdefault(value, []).append((i,j))

    antinodes = [[0 for _ in range(width)] for _ in range(height)]
    
    for key in ant_pos.keys():
        combs = itertools.combinations(ant_pos[key], 2)
        for comb in combs:
            for num, pos in enumerate(comb):
                k = -1
                while True:
                    k += 1
                    i = pos[0] + k*(comb[1][0] - comb[0][0])*((-1)**(num+1))
                    j = pos[1] + k*(comb[1][1] - comb[0][1])*((-1)**(num+1))

                    if (i >= 0) and (i < height) and (j >= 0) and (j < width):
                        antinodes[i][j] = 1
                    else:
                        break


    res = sum([sum(i) for i in antinodes])

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
    check_example(main, input_filename = "example_input.txt", answer_filename = "example_answer.txt")

    #run on the input
    main()

    check_example(main_2, input_filename = "example_input.txt", answer_filename = "example_answer_2.txt")

    # run on the input
    main_2()
