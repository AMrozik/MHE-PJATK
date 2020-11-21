import random
import json
import time
import sys


def join(list1):
    word = ""
    for char in list1:
        word += char
    return word


def load_data(file_name):
    try:
        with open(file_name, "r") as f:
            json_data = json.load(f)
            given_set = set(json_data)
            return given_set
    except FileNotFoundError:
        print("File Not Found")
        exit(1)


def save_to_file(file_name, given_set, solution, exec_time, score):
    with open(file_name, "w") as f:
        f.write(f"Dany zbiór: {given_set}\nZnalezione rozwiązanie: {solution}\nCzas wykonania algorytmu: {exec_time}\n"
                f"Wartość funkcji celu: {score}")


def read_mask(given_set, solution):
    mask = bin(0)

    for x in given_set:
        if x in solution:
            mask += "1"
        else:
            mask += "0"
    return mask[3:]


def next_solution(given_set, solution):
    max_mask = bin(2 ** len(given_set) - 1)
    mask_length = len(given_set)
    mask = read_mask(given_set, solution)

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
    # print("mask: ", next_mask)
    return set(next_sol)


# def negate_solution(given_set, solution):
#     max_mask = bin(2 ** len(given_set) - 1)
#     mask_length = len(given_set)
#     mask = read_mask(given_set, solution)
#
#     # xor with all ones (0b11111) to negate mask
#     negated_mask = bin(int(max_mask, 2) ^ int(mask, 2))[2:]
#
#     diff = mask_length - len(negated_mask)
#
#     negated_mask = str(negated_mask)
#
#     for i in range(diff):
#         negated_mask = "0" + str(negated_mask)
#
#     # print("negated mask: ", negated_mask)
#     negated_mask = str(negated_mask)
#
#     negated_sol = []
#     list_set = list(given_set)
#
#     for i in range(mask_length):
#         if negated_mask[i] == '1':
#             negated_sol.append(list_set[i])
#     # print("mask: ", prev_mask)
#     return set(negated_sol)


# def previous_solution(given_set, solution):
#     max_mask = bin(2 ** len(given_set) - 1)
#     mask_length = len(given_set)
#     mask = read_mask(given_set, solution)
#
#     if int(mask, 2) <= 1:
#         prev_mask = max_mask
#     else:
#         prev_mask = bin(int(mask, 2) - 1)
#
#     prev_mask = prev_mask[2:]
#
#     # fix mask - fill with zeros the oldest bits to max length
#     diff = mask_length - len(prev_mask)
#
#     prev_mask = str(prev_mask)
#
#     for i in range(diff):
#         prev_mask = "0" + str(prev_mask)
#
#     prev_sol = []
#     list_set = list(given_set)
#
#     for i in range(mask_length):
#         if prev_mask[i] == '1':
#             prev_sol.append(list_set[i])
#     # print("mask: ", prev_mask)
#     return set(prev_sol)


def generate_solution(given_set):
    mask_length = len(given_set)
    random_mask = ""
    for i in range(mask_length):
        random_mask += str(random.randint(0, 1))
    if "1" not in random_mask:
        random_mask = random_mask.replace("0", "1", 1)
    random_sol = []
    list_set = list(given_set)

    for i in range(mask_length):
        if random_mask[i] == '1':
            random_sol.append(list_set[i])
    return set(random_sol)


def generate_solution_surroundings(given_set, solution):

    surroundings = []
    mask = list(read_mask(given_set, solution))
    list_set = list(given_set)   # zmieniam zbior na liste zeby latwiej iterowac
    mask_length = len(given_set)

    # zmieniam po jednym bicie w masce na przeciwny
    for i in range(mask_length):
        sol = mask[:]   # kopia oryginalnej maski
        surr_sol = []   # wygenerowane rozwiazanie (podbior) na podstawie maski
        if sol[i] == '0':
            sol[i] = '1'
        else:
            sol[i] = '0'
        # print(sol)
        # generuje podzbior na podstawie maski
        for x in range(mask_length):
            if sol[x] == '1':
                surr_sol.append(list_set[x])
        # print(surr_sol)
        if len(surr_sol) > 0:
            surroundings.append(set(surr_sol))
    # print(surroundings)
    return surroundings

    # for i, bit in enumerate(mask):
    #     if bit == '0':
    #         mask[i] = '1'
    #     else:
    #         mask[i] = '0'

    # print(mask)

    # next_sol = next_solution(given_set, solution)
    # prev_sol = previous_solution(given_set, solution)
    # neg_sol = negate_solution(given_set, solution)
    # surroundings = [next_sol, next_solution(given_set, next_sol), prev_sol, previous_solution(given_set, prev_sol),
    #                 neg_sol, next_solution(given_set, neg_sol), previous_solution(given_set, neg_sol)]
    # return surroundings


def goal_function(subset):
    return abs(sum(subset))


def brute_force_solution(given_set):
    number_of_combinations = (2 ** len(given_set)) - 1
    solution = generate_solution(given_set)
    best_score = goal_function(solution)
    best = solution
    for x in range(number_of_combinations - 1):
        solution = next_solution(given_set, solution)
        solution_score = goal_function(solution)
        if solution_score < best_score:
            best_score = solution_score
            best = solution
    return best


def hill_climb(given_set):
    number_of_combinations = (2 ** len(given_set)) - 1
    solution = generate_solution(given_set)
    best_score = goal_function(solution)
    best_sol = solution
    found_better = False

    for i in range(number_of_combinations - 1):
        surrounding = generate_solution_surroundings(given_set, best_sol)
        for sol in surrounding:
            score = goal_function(sol)
            if score < best_score:
                found_better = True
                best_sol = sol
                best_score = score
        # # # DEBUG # # #
        print("i: ", i)
        # print("best solution:", best_sol)
        # print("best score: ", best_score)
        if best_score == 0:
            return best_sol
        if not found_better:
            return best_sol
        found_better = False
    return best_sol


if __name__ == '__main__':

    if len(sys.argv) > 2:
        test_set_file = sys.argv[1]
        solution_file = sys.argv[2]
    else:
        test_set_file = "the_killer_one.json"
        solution_file = "solution.txt"

    given_set = load_data("test sets/" + test_set_file)

    choose = input("Wybierz metodę:\n1: Brute Force\n2: Algorytm wspinaczkowy\n:")

    if choose == "1":
        chosen_fun = brute_force_solution
    elif choose == "2":
        chosen_fun = hill_climb
    else:
        exit(2)

    start_time = time.time()
    solution = chosen_fun(given_set)
    exec_time = time.time() - start_time
    score = goal_function(solution)

    print(f"Dany zbiór: {given_set}\nZnalezione rozwiązanie: {solution}\nCzas wykonania algorytmu: {exec_time}\n"
          f"Wartość funkcji celu: {score}")
    save_to_file(solution_file, given_set, solution, exec_time, score)

    # given_set = load_data("test sets/the_killer_one.json")
    # start_time = time.time()
    # solution = hill_climb(given_set)
    # exec_time = time.time() - start_time
    # print(f"Dany zbiór: {given_set}\nZnalezione rozwiązanie: {solution}\nCzas wykonania algorytmu: {exec_time}\n "
    #       f"Wartość funkcji celu: {goal_function(solution)}")
