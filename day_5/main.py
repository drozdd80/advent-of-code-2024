import os
import re

_path = os.path.dirname(__file__)


def read(path):
    with open(path, "r") as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split("\n")
    split_index = lines.index('')
    rules = lines[:split_index]
    pages = lines[split_index+1:]
    return rules, pages



def main(path=_path + "/input.txt", print_value=True):
    rules, pages = read(path)
    rules_split = [r.split('|') for r in rules]
    pages_split = [p.split(',') for p in pages]

    valid_pages = [1]*len(pages_split)
    for i, page in enumerate(pages_split):
        for rule in rules_split:
            if (rule[0] in page) & (rule[1] in page):
                if page.index(rule[0]) > page.index(rule[1]):
                    valid_pages[i] = 0
                    break
    
    res = 0
    for i, v in enumerate(valid_pages):
        if v == 1:
            page = pages_split[i]
            res += int(page[len(page)//2])
            

    if print_value:
        print(res)
    return res


def main_2(path=_path + "/input.txt", print_value=True):
    rules, pages = read(path)
    rules_split = [r.split('|') for r in rules]
    pages_split = [p.split(',') for p in pages]

    valid_pages = [1]*len(pages_split)
    for i, page in enumerate(pages_split):
        for rule in rules_split:
            if (rule[0] in page) & (rule[1] in page):
                if page.index(rule[0]) > page.index(rule[1]):
                    valid_pages[i] = 0
                    break
    
    for i, v in enumerate(valid_pages):
        if v == 0:
            page = pages_split[i]
            while True:
                v=1
                for rule in rules_split:
                    if (rule[0] in page) & (rule[1] in page):
                        ind1 = page.index(rule[0])
                        ind2 = page.index(rule[1])
                        if ind1 > ind2:
                            t = pages_split[i][ind1]
                            pages_split[i][ind1] = pages_split[i][ind2]
                            pages_split[i][ind2] = t
                            v=0
                            break
                if v == 1:
                    break

    res = 0
    for i, v in enumerate(valid_pages):
        if v == 0:
            page = pages_split[i]
            res += int(page[len(page)//2])
            
    if print_value:
        print(res)
    return res

if __name__ == "__main__":
    # validate on example
    example_calculation = main(_path + "/example_input.txt", print_value=False)
    with open(_path + "/example_answer.txt", "r") as input_data_file:
        example_answer = int(input_data_file.read())
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main()

    # validate on example
    example_calculation = main_2(_path + "/example_input.txt", print_value=False)
    with open(_path + "/example_answer_2.txt", "r") as input_data_file:
        example_answer = int(input_data_file.read())
    assert (
        example_calculation == example_answer
    ), f"Calculation {example_calculation} is different from example answer {example_answer}"

    # run on the input
    main_2()
