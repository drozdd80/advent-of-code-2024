import os
import numpy as np

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    items = [[char for char in line] for line in lines]
    return items



def main(path=_path + "/input.txt", print_value=True):
    input = read(path)

    start_i = -1
    start_j = -1
    for i, l in enumerate(input):
        for j, v in enumerate(l):
            if v == '^':
                start_i = i
                start_j = j

    rotation_matrix = np.array([[0, 1],
                                [-1,  0]])

    size_i = len(input)
    size_j = len(input[0])

    direction = np.array([-1, 0])
    dir_count = 0
    i = start_i
    j = start_j
    res = 0
    while True:
        if input[i][j] != "X":
            res += 1
        input[i][j] = "X"
        if (i+direction[0] >= size_i) or (i+direction[0] < 0) or (j+direction[1] >= size_j) or (j+direction[1] < 0):
            break
        elif input[i+direction[0]][j+direction[1]] != "#":
            i += direction[0]
            j += direction[1]
        else:
            direction = np.dot(rotation_matrix, direction)

    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    input = read(path)
    
    raw_input = read(path)

    start_i = -1
    start_j = -1
    for i, l in enumerate(input):
        for j, v in enumerate(l):
            if v == '^':
                start_i = i
                start_j = j

    rotation_matrix = np.array([[0, 1],
                                [-1,  0]])

    size_i = len(input)
    size_j = len(input[0])

    direction = np.array([-1, 0])
    i = start_i
    j = start_j
    res = 0


    while True:
        if input[i][j] != "X":
            res += 1
        input[i][j] = "X"
        if (i+direction[0] >= size_i) or (i+direction[0] < 0) or (j+direction[1] >= size_j) or (j+direction[1] < 0):
            break
        elif input[i+direction[0]][j+direction[1]] != "#":
            i += direction[0]
            j += direction[1]
        else:
            direction = np.dot(rotation_matrix, direction)

    paths = []
    for i, row in enumerate(input):
        for j, val in enumerate(row):
            if (val == 'X') & ((i != start_i) or (j != start_j)):
                paths.append([i,j])
                
    dir_count = 0
    loop = 0
    for ii, jj in paths:
        input_2 = read(path)
        input_2[ii][jj] = '#'
        i = start_i
        j = start_j
        direction = np.array([-1, 0])
        dir_count=0
        dirs = [[set() for _ in range(len(input_2[0]))] for _ in range(len(input_2))]
        print(ii, jj)
        while True:
            if (input_2[i][j] != "0") and (input_2[i][j] != "1") and (input_2[i][j] != "2") and (input_2[i][j] != "3"):
                res += 1
            input_2[i][j] = str(dir_count)
            dirs[i][j].add(dir_count)
            if (i+direction[0] >= size_i) or (i+direction[0] < 0) or (j+direction[1] >= size_j) or (j+direction[1] < 0):
                break
            if dir_count in dirs[i+direction[0]][j+direction[1]]:
                loop += 1
                break
            elif input_2[i+direction[0]][j+direction[1]] != "#":
                i += direction[0]
                j += direction[1]

            else:
                direction = np.dot(rotation_matrix, direction)
                dir_count = (dir_count + 1)%4
                
    if print_value:
        print(loop)

    return loop

if __name__ == "__main__":
    # validate on example
    example_calculation = main(_path + "/example_input.txt", print_value=False)
    with open(_path + "/example_answer.txt", "r") as input_data_file:
        example_answer = int(input_data_file.read())
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main()

    # validate on example
    example_calculation = main_2(_path + "/example_input.txt", print_value=False)
    with open(_path + "/example_answer_2.txt", "r") as input_data_file:
        example_answer = int(input_data_file.read())
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main_2()
