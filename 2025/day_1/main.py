import os

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    items = [(line[0], int(line[1:])) for line in lines]
    return items       


def main(path=_path + "/input.txt", print_value=True):
    inputs = read(path)

    total = 50
    res = 0
    shifts = [(-1)**int(v[0] == 'L')*v[1]  for v in inputs]
    totals = [total]
    for shift in shifts:
        total = (total + shift)%100
        totals.append(total)
        if total == 0:
            res += 1

    if print_value:
        print(res)
    return res


# def main_2(path=_path + "/input.txt", print_value=True):
#     input = read(path)

#     res = 0

#     if print_value:
#         print(res)
#     return res


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
    main(print_value=True)

    # check_example(main_2, input_filename = "example_input.txt", answer_filename = "example_answer_2.txt")

    # #run on the input
    # main_2()