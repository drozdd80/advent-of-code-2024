import os
import re

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    return lines



def main(path=_path + "/input.txt", print_value=True):
    input = read(path)

    row_n = len(input)
    col_n = len(input[0])

    res = 0

    for row in range(row_n):
        for col in range(col_n):
            if input[row][col] == 'X':
                if (row+3 < row_n):
                    if input[row][col] + input[row+1][col] + input[row+2][col] + input[row+3][col] == 'XMAS':
                        res+=1
                if (row+3 < row_n) & (col+3 < col_n):
                    if input[row][col] + input[row+1][col+1] + input[row+2][col+2] + input[row+3][col+3] == 'XMAS':
                        res+=1
                if (col+3 < col_n):
                    if input[row][col] + input[row][col+1] + input[row][col+2] + input[row][col+3] == 'XMAS':
                        res+=1
                if (row-3 >= 0) & (col+3 < col_n):
                    if input[row][col] + input[row-1][col+1] + input[row-2][col+2] + input[row-3][col+3] == 'XMAS':
                        res+=1
                if (row-3 >= 0):
                    if input[row][col] + input[row-1][col] + input[row-2][col] + input[row-3][col] == 'XMAS':
                        res+=1
                if (row-3 >= 0) & (col-3 >= 0):
                    if input[row][col] + input[row-1][col-1] + input[row-2][col-2] + input[row-3][col-3] == 'XMAS':
                        res+=1
                if (col-3 >= 0):
                    if input[row][col] + input[row][col-1] + input[row][col-2] + input[row][col-3] == 'XMAS':
                        res+=1
                if (row+3 < row_n) & (col-3 >= 0):
                    if input[row][col] + input[row+1][col-1] + input[row+2][col-2] + input[row+3][col-3] == 'XMAS':
                        res+=1

    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    input = read(path)

    row_n = len(input)
    col_n = len(input[0])

    res = 0

    for row in range(row_n):
        for col in range(col_n):
            if input[row][col] == 'A':
                if ((row+1 < row_n) & (row-1 >= 0) & (col+1 < col_n) & (col-1 >= 0)):
                    word1 = input[row+1][col+1] + input[row][col] + input[row-1][col-1]
                    word2 = input[row+1][col-1] + input[row][col] + input[row-1][col+1]
                    if ((word1 == 'MAS') or (word1 == 'SAM')) and ((word2 == 'MAS') or (word2 == 'SAM')):
                        res+=1

    if print_value:
        print(res)
    return res

if __name__ == "__main__":
    # validate on example
    example_calculation = main(_path + "/example_input.txt", print_value=False)
    example_answer = int(read(_path + "/example_answer.txt")[0])
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main()

    # validate on example
    example_calculation = main_2(_path + "/example_input.txt", print_value=False)
    example_answer = int(read(_path + "/example_answer_2.txt")[0])
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main_2()
