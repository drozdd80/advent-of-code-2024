import os
import re
import math

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    lines_parsed = []
    for line in lines:
        pos = re.findall("p\=(\-?\d+)\,(\-?\d+)", line)[0]
        vel = re.findall("v\=(\-?\d+)\,(\-?\d+)", line)[0]
        lines_parsed.append([[int(pos[0]), int(pos[1])], [int(vel[0]), int(vel[1])]])
    return lines_parsed

def main(path=_path + "/input.txt", print_value=True, width = 101, height = 103, iterations = 100):
    input = read(path)

    new_pos = []
    for robot in input:
        px = robot[0][0]
        py = robot[0][1]
        vx = robot[1][0]
        vy = robot[1][1]
        
        new_px = (px+vx*iterations)%width
        new_py = (py+vy*iterations)%height

        quadrant = None
        if (new_px < math.floor(width/2)) and (new_py < math.floor(height/2)):
            quadrant = 0
        elif (new_px > math.floor(width/2)) and (new_py < math.floor(height/2)):
            quadrant = 1
        elif (new_px < math.floor(width/2)) and (new_py > math.floor(height/2)):
            quadrant = 2
        elif (new_px > math.floor(width/2)) and (new_py > math.floor(height/2)):
            quadrant = 3

        new_pos.append((new_px, new_py, quadrant))

    res=1
    for i in range(4):
        res *= len([pos[2] for pos in new_pos if pos[2]==i])

    mymap = [['.' for _ in range(width)] for _ in range(height)]

    for pos in new_pos:
        mymap[pos[1]][pos[0]] = '*'

    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True, width = 101, height = 103, iterations = 100):
    input = read(path)

    new_pos = []
    for robot in input:
        px = robot[0][0]
        py = robot[0][1]
        vx = robot[1][0]
        vy = robot[1][1]
        
        new_px = (px+vx*iterations)%width
        new_py = (py+vy*iterations)%height

        quadrant = None
        if (new_px < math.floor(width/2)) and (new_py < math.floor(height/2)):
            quadrant = 0
        elif (new_px > math.floor(width/2)) and (new_py < math.floor(height/2)):
            quadrant = 1
        elif (new_px < math.floor(width/2)) and (new_py > math.floor(height/2)):
            quadrant = 2
        elif (new_px > math.floor(width/2)) and (new_py > math.floor(height/2)):
            quadrant = 3

        new_pos.append((new_px, new_py, quadrant))

    res=1
    for i in range(4):
        res *= len([pos[2] for pos in new_pos if pos[2]==i])

    mymap = [['.' for _ in range(width)] for _ in range(height)]

    for pos in new_pos:
        mymap[pos[1]][pos[0]] = '*'

    if len(new_pos) - len(set(new_pos)) < 2:
        print(iterations)
        print('\n'.join([''.join(line) for line in  mymap]))

    return res


def check_example(func, input_filename = "example_input.txt", answer_filename = "example_answer.txt", **kwargs):
    example_calculation = func(_path + "/" + input_filename, print_value=False, **kwargs)
    with open(_path + "/" + answer_filename, "r") as input_data_file:
        example_answer = int(input_data_file.read())
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

if __name__ == "__main__":
    check_example(main, input_filename = "example_input.txt", answer_filename = "example_answer.txt", width=11, height=7)

    #run on the input
    main()

    # check_example(main_2, input_filename = "example_input.txt", answer_filename = "example_answer_2.txt")

    # #run on the input
    file_name = "output.txt"
    open(file_name, 'w').close()
    i = 0
    while i < 10000:
        i += 1
        main_2(iterations = i)