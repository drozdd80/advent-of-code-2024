import os
from operator import add, mul
import itertools

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    items = [line.split(':') for line in lines]
    return [[int(item[0]), [int(it) for it in item[1].strip().split(" ")]] for item in items]


def concat(a, b):
    return int(str(a) + str(b))

def check_if_valid(numbers, result, actions):
    combinations =  itertools.product(actions, repeat=len(numbers)-1)
    for combination in combinations:
        res = numbers[0]
        for i, func in enumerate(combination):
            res = func(res, numbers[i+1])
        if res == result:
            return True
    return False
        


def main(path=_path + "/input.txt", print_value=True):
    input = read(path)
    res = 0
    actions = [add, mul]
    for line in input:
        if check_if_valid(numbers=line[1], result=line[0], actions = actions):
            res += line[0]
    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    input = read(path)
    res = 0
    actions = [add, mul, concat]
    for line in input:
        if check_if_valid(numbers=line[1], result=line[0], actions = actions):
            res += line[0]
    if print_value:
        print(res)
    return res

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
