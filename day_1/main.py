import os

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    split_lines = [f.split() for f in lines]
    return split_lines


def main(path=_path + "/input.txt", print_value=True):
    input = read(path)
    col1 = sorted([v[0] for v in input])
    col2 = sorted([v[1] for v in input])
    values = [abs(int(col2[i]) - int(col1[i])) for i in range(len(col1))]
    res = sum(values)
    if print_value:
        print(res)
    return res

def main_2(path=_path + "/input.txt", print_value=True):
    from collections import Counter
    input = read(path)
    col1 = [int(v[0]) for v in input]
    col2 = [int(v[1]) for v in input]
    
    res = sum([Counter(col2)[val1]*val1 for val1 in col1])
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
    main_2(_path + "/example_input.txt", print_value=False)
    main_2()
