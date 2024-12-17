import os

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    i = lines.index('')
    path = [char for char in ''.join(lines[i+1:])]
    lines_map = lines[:i]
    items = [[char for char in line] for line in lines_map]

    return path, items     

def transform_path(path):
    replacements = {
        "<" : (0,-1),
        "^": (-1, 0),
        ">": (0,1),
        "v": (1, 0)
    }
    return [replacements.get(x, x) for x in path]


def main(path=_path + "/input.txt", print_value=True):
    path, pos_map = read(path)
    t_path = transform_path(path)

    si = None
    sj = None
    for i, line in enumerate(pos_map):
        for j, char in enumerate(line):
            if char == '@':
                si = i
                sj = j
                break
    
    for count, (di, dj) in enumerate(t_path):
        ci = si + di
        cj = sj + dj
        if pos_map[ci][cj] == "#":
            pass
        elif pos_map[ci][cj] == '.':
            pos_map[ci][cj] =  pos_map[si][sj]
            pos_map[si][sj] = '.'
            si = ci
            sj = cj
            pass
        elif pos_map[ci][cj] == 'O':
            k = 1
            while pos_map[ci][cj] == 'O':
                k+=1
                ci = si + k*di
                cj = sj + k*dj
            if pos_map[ci][cj] == "#":
                pass
            elif pos_map[ci][cj] == '.':
                for kk in range(k-1, -1, -1):
                    pos_map[ci][cj] = pos_map[si + kk*di][sj + kk*dj]
                    pos_map[si + kk*di][sj + kk*dj] = '.'
                    ci = si + kk*di
                    cj = sj + kk*dj
                pos_map[si][sj] = '.'
                si += di
                sj += dj
        #print(count)
        #print('\n'.join([''.join(line) for line in pos_map]))

    box_pos = []
    for i, line in enumerate(pos_map):
        for j, char in enumerate(line):
            if char == 'O':
                box_pos.append((i,j))

    res = sum([100*i + j for i, j in box_pos])

    if print_value:
        print(res)
    return res

# def read_2(path):
#     with open(path, "r") as input_data_file:
#         input_data = input_data_file.read()
#     lines = input_data.split("\n")
#     i = lines.index('')
#     path = [char for char in ''.join(lines[i+1:])]
#     lines_map = lines[:i]
#     for i, line in enumerate(lines_map):
#         lines_map[i] = [line[int(2*i)] + line[int(2*i+1)] for i in range(int(len(line)/2))]
#     items = [[char for char in line] for line in lines_map]

#     return path, items 

def read2(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    i = lines.index('')
    path = [char for char in ''.join(lines[i+1:])]
    lines_map = lines[:i]
    items = [[char for char in line.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')] for line in lines_map]

    return path, items  

def get_next_row(pos_map, current_row_coord, di):
    next_row_coord = [(ci+di, cj) for ci, cj in current_row_coord]
    next_row_values = [pos_map[ci][cj] for ci, cj in next_row_coord]
    if '#' in next_row_values:
        return False, pos_map, current_row_coord
    elif set(next_row_values) == set(['.']):
        #import ipdb; ipdb.set_trace()
        for ci, cj in current_row_coord:
            pos_map[ci + di][cj] = pos_map[ci][cj]
            pos_map[ci][cj] = '.'   
        return True, pos_map, next_row_coord
    if next_row_values[0] == ']':
        next_row_coord = [(next_row_coord[0][0], next_row_coord[0][1] - 1)] + next_row_coord
        next_row_values = ['['] + next_row_values
    if next_row_values[-1] == '[':
        next_row_coord = next_row_coord + [(next_row_coord[-1][0], next_row_coord[-1][1] + 1)]
        next_row_values = next_row_values + [']']
    next_res, pos_map, _ = get_next_row(pos_map, next_row_coord, di)
    if next_res:
        return get_next_row(pos_map, current_row_coord, di)
    return False, pos_map, current_row_coord


def main_2(path=_path + "/input.txt", print_value=True):
    path, pos_map = read2(path)
    t_path = transform_path(path)

    si = None
    sj = None
    for i, line in enumerate(pos_map):
        for j, char in enumerate(line):
            if char == '@':
                si = i
                sj = j
                break
    for count, (di, dj) in enumerate(t_path):
        # if count % 10 == 9:
        #     import ipdb; ipdb.set_trace()
        ci = si + di
        cj = sj + dj
        if pos_map[ci][cj] == "#":
            pass
        elif pos_map[ci][cj] == '.':
            pos_map[ci][cj] =  pos_map[si][sj]
            pos_map[si][sj] = '.'
            si = ci
            sj = cj
            pass
        elif di == 0:

            if (pos_map[ci][cj] == '[') or (pos_map[ci][cj] == ']'):
                k = 1
                while (pos_map[ci][cj] == '[') or (pos_map[ci][cj] == ']'):
                    k+=1
                    ci = si + k*di
                    cj = sj + k*dj
                if pos_map[ci][cj] == "#":
                    pass
                elif pos_map[ci][cj] == '.':
                    for kk in range(k-1, -1, -1):
                        pos_map[ci][cj] = pos_map[si + kk*di][sj + kk*dj]
                        pos_map[si + kk*di][sj + kk*dj] = '.'
                        ci = si + kk*di
                        cj = sj + kk*dj
                    pos_map[si][sj] = '.'
                    si += di
                    sj += dj
        else:
            _, _, [(si, sj)] = get_next_row(pos_map, [(si, sj)], di)
        print(count)
        print('\n'.join([''.join(line) for line in pos_map]))

    box_pos = []
    for i, line in enumerate(pos_map):
        for j, char in enumerate(line):
            if char == '[':
                box_pos.append((i,j))

    res = sum([100*i + j for i, j in box_pos])

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
    # check_example(main, input_filename = "example_input_2.txt", answer_filename = "example_answer_2.txt")


    # #run on the input
    # main()

    check_example(main_2, input_filename = "example_input.txt", answer_filename = "example_answer_5.txt")

    # #run on the input
    #main_2()