import os
from operator import add, mul
import itertools
from tqdm import tqdm

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    return input_data        


def main(path=_path + "/input.txt", print_value=True):
    input = read(path)

    decripted = []
    for i, char in enumerate(input):

        if i % 2 ==0:
            ix = i//2
            decripted.extend([ix for _ in range(int(char))])
        else:
            decripted.extend(['' for _ in range(int(char))])

    reversed_decripted = decripted[::-1]

    values_to_move_gen = (i for i, v in enumerate(reversed_decripted) if v != '')

    for i in values_to_move_gen:
        ind_empty = decripted.index('')
        ind_value = len(decripted) - i - 1
        if ind_value > ind_empty:
            decripted[ind_empty], decripted[ind_value] = decripted[ind_value], decripted[ind_empty]
        else:
            break

    res = sum([i*v for i, v in enumerate(decripted) if v != ''])

    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    input = read(path)

    decripted = []
    for i, char in enumerate(input):

        if i % 2 ==0:
            ix = i//2
            decripted.extend([ix for _ in range(int(char))])
        else:
            decripted.extend(['.' for _ in range(int(char))])

    reversed_decripted = decripted[::-1]
    unique_values = list(set(reversed_decripted))
    unique_values.remove('.')
    vpos = {}
    for v in unique_values:
        start = decripted.index(v)
        end = len(decripted) - reversed_decripted.index(v) - 1
        vpos[v] = (start, end)

    for v in tqdm(sorted(unique_values, reverse=True)):
        size = vpos[v][1] - vpos[v][0] + 1
        window = 0
        first_empty_ind = decripted.index('.')
        if size+first_empty_ind <= len(decripted):
            for i in range(first_empty_ind, size+first_empty_ind):
                if decripted[i] != '.':
                    window += 1
            if (window == 0) and (vpos[v][0] > first_empty_ind + size - 1):
                for i in range(first_empty_ind, size+first_empty_ind):
                    j = i - first_empty_ind
                    decripted[i], decripted[vpos[v][0] + j] = decripted[vpos[v][0] + j], decripted[i]
            else:
                for i in range(1+first_empty_ind, vpos[v][0]-size+1):
                    next_window_change = 0 if decripted[i + size - 1] == '.' else 1
                    prev_window_change = 0 if decripted[i-1] == '.' else 1
                    window += next_window_change - prev_window_change
                    if window == 0:
                        for j in range(size):
                            decripted[i+j], decripted[vpos[v][0] + j] = decripted[vpos[v][0] + j], decripted[i+j]
                        break
                
    res = sum([i*v for i, v in enumerate(decripted) if v != '.'])

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

    check_example(main_2, input_filename = "example_input_3.txt", answer_filename = "example_answer_3.txt")

    #run on the input
    main_2()