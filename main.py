import random
import json
import time
import sys


def load_data(file_name):
    with open(file_name, "r") as f:
        json_data = json.load(f)
        given_set = set(json_data)
        return given_set


def save_to_file(file_name, given_set, solution, time):
    with open(file_name, "w") as f:
        f.write(f"Dany zbiór: {given_set}\nZnalezione rozwiązanie: {solution}\nCzas wykonania algorytmu: {time}")


def next_solution(given_set, solution):
    max_mask = bin(2 ** len(given_set) - 1)
    mask_length = len(given_set)
    mask = bin(0)

    for x in given_set:
        if x in solution:
            mask += "1"
        else:
            mask += "0"

    if int(mask, 2) >= int(max_mask, 2):
        next_mask = bin(1)
    else:
        next_mask = bin(int(mask, 2) + 1)

    next_mask = next_mask[2:]

    # fix mask - fill with zeros the oldest bits to max length
    diff = mask_length - len(next_mask)

    next_mask = str(next_mask)

    for i in range(diff):
        next_mask = "0" + str(next_mask)

    next_sol = []
    list_set = list(given_set)

    for i in range(mask_length):
        if next_mask[i] == '1':
            next_sol.append(list_set[i])
    return set(next_sol)


def generate_solution(given_set):
    mask_length = len(given_set)
    random_mask = ""
    for i in range(mask_length):
        random_mask += str(random.randint(0,1))
    random_sol = []
    list_set = list(given_set)

    for i in range(mask_length):
        if random_mask[i] == '1':
            random_sol.append(list_set[i])
    return set(random_sol)


def goal_function(subset):
    return sum(subset)


def brute_force_solution(given_set):
    number_of_combinations = (2**len(given_set))-1
    solution = generate_solution(given_set)
    best_score = goal_function(solution)
    best = solution
    for x in range(number_of_combinations-1):
        solution = next_solution(given_set, solution)
        solution_score = goal_function(solution)
        if abs(solution_score) < abs(best_score):
            best_score = solution_score
            best = solution
    return best


if __name__ == '__main__':

    if len(sys.argv) > 2:
        test_set_file = sys.argv[1]
        solution_file = sys.argv[2]
    else:
        test_set_file = "set1.json"
        solution_file = "solution.txt"

    given_set = load_data("test sets/"+test_set_file)
    print("Dany zbiór wejściowy: ", given_set)

    start_time = time.time()
    solution = brute_force_solution(given_set)
    exec_time = time.time() - start_time

    print(f"Dany zbiór: {given_set}\nZnalezione rozwiązanie: {solution}\nCzas wykonania algorytmu: {time}")
    save_to_file(solution_file, given_set, solution, exec_time)



