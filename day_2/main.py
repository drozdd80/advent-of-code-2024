import os

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    split_lines = [f.split() for f in lines]
    return split_lines


def is_safe(line):
    diff = [line[j + 1] - line[j] for j in range(len(line) - 1)]
    if ((max(diff) <= 3) & (min(diff) >= 1)) or ((max(diff) <= -1) & (min(diff) >= -3)):
        return True
    return False


def main(path=_path + "/input.txt", print_value=True):
    input = read(path)
    for i, ii in enumerate(input):
        input[i] = [int(j) for j in ii]

    res = 0
    for line in input:
        if is_safe(line):
            res += 1

    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    input = read(path)
    for i, ii in enumerate(input):
        input[i] = [int(j) for j in ii]

    res = 0
    for line in input:
        for i, _ in enumerate(line):
            line_without_i = line[:i] + line[i + 1 :]
            if is_safe(line_without_i):
                res += 1
                break

    if print_value:
        print(res)
    return res


if __name__ == "__main__":
    # validate on example
    example_calculation = main(_path + "/example_input.txt", print_value=False)
    example_answer = int(read(_path + "/example_answer.txt")[0][0])
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main()

    # validate on example
    example_calculation = main_2(_path + "/example_input.txt", print_value=False)
    example_answer = int(read(_path + "/example_answer_2.txt")[0][0])
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main_2()
