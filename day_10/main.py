import os
import itertools
from tqdm import tqdm

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    items = [[int(char) for char in line] for line in lines]
    return items       

def in_limits(i, j, height, width):
    return (i >= 0) and (i < height) and (j >=0) and (j < width)

def rr(field, res, i, j, height, width, last_value, path, paths, trainends):
    path=path[:]
    if in_limits(i, j, height, width):
        current_value = field[i][j]
        if current_value - last_value == 1:
            path.append((i,j))
            if field[i][j] == 9:
                if (i,j) not in trainends:
                    trainends.append((i,j))
                    res += 1
                paths.append(path)
                return res
            else:
                res = rr(field, res, i=i+1, j=j, height=height, width=width, last_value=current_value, path=path, paths=paths, trainends=trainends)
                res = rr(field, res, i=i, j=j+1, height=height, width=width, last_value=current_value, path=path, paths=paths, trainends=trainends)
                res = rr(field, res, i=i-1, j=j, height=height, width=width, last_value=current_value, path=path, paths=paths, trainends=trainends)
                res = rr(field, res, i=i, j=j-1, height=height, width=width, last_value=current_value, path=path, paths=paths, trainends=trainends)
    return res

def rr2(field, res, i, j, height, width, last_value, path, paths):
    path=path[:]
    if in_limits(i, j, height, width):
        current_value = field[i][j]
        if current_value - last_value == 1:
            path.append((i,j))
            if field[i][j] == 9:
                res += 1
                paths.append(path)
                return res
            else:
                res = rr2(field, res, i=i+1, j=j, height=height, width=width, last_value=current_value, path=path, paths=paths)
                res = rr2(field, res, i=i, j=j+1, height=height, width=width, last_value=current_value, path=path, paths=paths)
                res = rr2(field, res, i=i-1, j=j, height=height, width=width, last_value=current_value, path=path, paths=paths)
                res = rr2(field, res, i=i, j=j-1, height=height, width=width, last_value=current_value, path=path, paths=paths)
    return res

def draw_path(path):
    height = 8
    width = 8
    map = [['.' for _ in range(width)] for _ in range(height)]
    for k,(i,j) in enumerate(path):
        map[i][j] = k
    print('\n'.join([''.join([str(char) for char in line]) for line in map]))

def main(path=_path + "/input.txt", print_value=True):
    field = read(path)
    height = len(field)
    width = len(field[0])
    paths = []
    res=0
    trainends_all = {}
    for i in range(height):
        for j in range(width):
            if field[i][j] == 0:
                trainends_all[(i,j)] = []
                res += rr(field=field, res=0, i=i, j=j, height=height, width=width, last_value=-1, path=[], paths=paths, trainends=trainends_all[(i,j)])

    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    field = read(path)
    height = len(field)
    width = len(field[0])
    paths = []
    res=0
    for i in range(height):
        for j in range(width):
            if field[i][j] == 0:
                res += rr2(field=field, res=0, i=i, j=j, height=height, width=width, last_value=-1, path=[], paths=paths)

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

    #run on the input
    main_2()