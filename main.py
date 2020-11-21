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


def tabu_search(given_set, max_interations, max_tabu_size):
    solution = generate_solution(given_set)
    best_score = goal_function(solution)
    best_sol = solution
    tabu_list = []
    tabu_list.append(solution)

    for i in range(max_interations):
        surrounding = generate_solution_surroundings(given_set, best_sol)
        bestCandidate = surrounding[0]
        for candidate in surrounding:
            if candidate not in tabu_list and goal_function(candidate) < goal_function(bestCandidate):
                bestCandidate = candidate
        if goal_function(bestCandidate) < goal_function(best_sol):
            best_sol = bestCandidate
        tabu_list.append(bestCandidate)
        if len(tabu_list) > max_tabu_size:
            tabu_list.pop()
    return best_sol


if __name__ == '__main__':

    # if len(sys.argv) > 2:
    #     test_set_file = sys.argv[1]
    #     solution_file = sys.argv[2]
    # else:
    #     test_set_file = "the_killer_one.json"
    #     solution_file = "solution.txt"
    #
    # given_set = load_data("test sets/" + test_set_file)
    #
    # choose = input("Wybierz metodę:\n1: Brute Force\n2: Algorytm wspinaczkowy\n:3: Wyszukiwanie Tabu\n:")
    #
    # if choose == "1":
    #     chosen_fun = brute_force_solution
    # elif choose == "2":
    #     chosen_fun = hill_climb
    # elif choose == "3":
    #     chosen_fun = tabu_search
    # else:
    #     exit(2)
    #
    # start_time = time.time()
    # solution = chosen_fun(given_set)
    # exec_time = time.time() - start_time
    # score = goal_function(solution)
    #
    # print(f"Dany zbiór: {given_set}\nZnalezione rozwiązanie: {solution}\nCzas wykonania algorytmu: {exec_time}\n"
    #       f"Wartość funkcji celu: {score}")
    # save_to_file(solution_file, given_set, solution, exec_time, score)

    given_set = load_data("test sets/the_killer_one.json")
    start_time = time.time()
    solution = tabu_search(given_set, 200, 10)
    exec_time = time.time() - start_time
    print(f"Dany zbiór: {given_set}\nZnalezione rozwiązanie: {solution}\nCzas wykonania algorytmu: {exec_time}\n "
          f"Wartość funkcji celu: {goal_function(solution)}")
