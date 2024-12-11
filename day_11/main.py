import os

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    items = [line.split(' ') for line in lines]
    return [[int(char) for char in line] for line in items][0]       

def apply_rules(x):
    n_digits = len(str(x))
    if x == 0:
        return [1]
    elif n_digits%2 == 0:
        n1 = int(str(x)[:int(n_digits/2)])
        n2 = int(str(x)[int(n_digits/2):])
        return [n1, n2]
    else:
        return [x*2024]

def update_dict(x, d, i, limit):
    if i <= limit:
        if x not in d:
            d[x] = [apply_rules(x), i]
        if i <= d[x][1]:
            for v in d[x][0]:
                update_dict(v, d, i+1, limit)



def browse_dict(x, d, i, limit, res, ans):
    if i == limit-1:
        #res += len(d[x][0])
        ans.extend(d[x][0])
    else:
        for v in d[x][0]:
            browse_dict(v, d, i+1, limit, res, ans)


def main(path=_path + "/input.txt", print_value=True):
    input = read(path)
    
    transformation_dict = {}
    ans = []
    limit = 25
    for value in input:
        update_dict(value, transformation_dict, 0, limit)
    
    for value in input:
         browse_dict(value, transformation_dict, 0, limit, 0, ans)
    result = len(ans)

    if print_value:
        print(result)
    return result


def precompute_stones(transformation_dict, limit):
    precomputed_stone_n = {node: [0] * (limit + 1) for node in transformation_dict}

    for node in transformation_dict:
        precomputed_stone_n[node][0] = 1

    for depth in range(1, limit + 1):
        for node, (stone, _) in transformation_dict.items():
            precomputed_stone_n[node][depth] = sum(precomputed_stone_n[neighbor][depth - 1] for neighbor in stone)

    return precomputed_stone_n

def count_paths(input, precomputed_stone_n, limit):
    total_stones = 0
    for node in input:
        total_stones += precomputed_stone_n.get(node, [0] * (limit + 1))[limit]
    return total_stones

def main_2(path=_path + "/input.txt", print_value=True):
    input = read(path)
    
    transformation_dict = {}
    limit = 75
    for value in input:
        update_dict(value, transformation_dict, 0, limit)

    precomputed_paths = precompute_stones(transformation_dict, limit)
    result = count_paths(input, precomputed_paths, limit)

    if print_value:
        print(result)
    return result


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
    main_2()