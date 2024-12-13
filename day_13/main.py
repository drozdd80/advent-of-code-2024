import os
import re
from sympy import Matrix

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    input_dicts = []
    i = 0
    k = 0

    while i+2 < len(lines):
        k+=1
        if lines[i].startswith('Button A'):
            input_dict = {'A': {}, 'B': {}, 'Prize': {}}
            input_dict['A']['X'] = int(re.findall("X\+(\d+)", lines[i])[0])
            input_dict['A']['Y'] = int(re.findall("Y\+(\d+)", lines[i])[0])
            input_dict['B']['X'] = int(re.findall("X\+(\d+)", lines[i+1])[0])
            input_dict['B']['Y'] = int(re.findall("Y\+(\d+)", lines[i+1])[0])
            input_dict['Prize']['Y'] = int(re.findall("Y\=(\d+)", lines[i+2])[0])
            input_dict['Prize']['X'] = int(re.findall("X\=(\d+)", lines[i+2])[0])
        input_dicts.append(input_dict)
        i+=4
    return input_dicts       

def cramer_rule(A, B):
    det_A = A.det()
    if det_A == 0:
        return False

    solutions = []
    for i in range(A.shape[0]):
        Ai = A.copy()
        Ai[:, i] = B
        solutions.append(Ai.det() / det_A)

    return solutions

def main(path=_path + "/input.txt", print_value=True):
    input_dicts = read(path)
    valid_solutions = []
    for play in input_dicts:

        A = Matrix([[play['A']['X'], play['B']['X']],
                    [play['A']['Y'], play['B']['Y']]
                    ])
        B = Matrix([play['Prize']['X'], play['Prize']['Y']])
        solution = cramer_rule(A, B)  
        if len(solution) == 1:
            solution = [play['Prize']['X']/play['B']['X'], play['Prize']['Y']/play['B']['Y']]
        if (solution[0] == int(solution[0])) and (solution[1] == int(solution[1])):
            solution = [int(sol) for sol in solution]
            valid_solutions.append(solution)
    res = sum([sol[0]*3 + sol[1] for sol in valid_solutions])  

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
    main()

    # check_example(main_2, input_filename = "example_input.txt", answer_filename = "example_answer_2.txt")

    # #run on the input
    # main_2()