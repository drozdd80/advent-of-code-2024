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


def main_2(path=_path + "/input.txt", print_value=True):
    inputs = read(path)

    last_total=50
    total = 50
    res = 0
    shifts = [(-1)**int(v[0] == 'L')*v[1]  for v in inputs]
    totals = [total]
    for i, shift in enumerate(shifts):
        last_total = total
        total = (total + shift)

        if last_total == 0 and total//100 < 0:
            res -= 1
        res += abs(total//100)
        if total == 0:
            res +=1

        totals.append(total%100)
        total = total%100


    # import pdb; pdb.set_trace()
    print(totals)
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
    # check_example(main, input_filename = "example_input.txt", answer_filename = "example_answer.txt")

    # #run on the input
    # main()

    check_example(main_2, input_filename = "example_input_2.txt", answer_filename = "example_answer_3.txt")

    #run on the input
    main_2()