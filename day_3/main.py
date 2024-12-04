import os
import re

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    return input_data


def find_mult_sum(input):
    number_tuples = re.findall("mul\((\d+),(\d+)\)", input)
    return sum([int(num[0]) * int(num[1]) for num in number_tuples])


def main(path=_path + "/input.txt", print_value=True):
    input = read(path)
    res = find_mult_sum(input)
    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    input = read(path)

    # manually add start and end breaking words to avoid accounting for several cases
    input = "do()" + input + "don't()"

    middle_block_pattern = r"do\(\)([\s\S]*?)don't\(\)"

    blocks = re.findall(middle_block_pattern, input)

    res = 0
    for block in blocks:
        res += find_mult_sum(block)
    if print_value:
        print(res)
    return res


if __name__ == "__main__":
    # validate on example
    example_calculation = main(_path + "/example_input.txt", print_value=False)
    example_answer = int(read(_path + "/example_answer.txt"))
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main()

    # validate on example
    example_calculation = main_2(_path + "/example_input_2.txt", print_value=False)
    example_answer = int(read(_path + "/example_answer_2.txt"))
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main_2()
