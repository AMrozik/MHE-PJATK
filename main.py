from itertools import combinations
import random
import json


def load_data(file_name):
    with open("set2.json", "r") as f:
        json_data = json.load(f)
        given_set = set(json_data)
        return given_set


# goal - suma elementów danego podzbioru

# generate_solution - generuj losowe rozwiązanie (nie musi być poprawne?)

# każdej liczbie w zbiorze odpowiada 0 lub 1 - maska
# na podstawie tej maski moge wygenerować kolejne rozwiązanie


def generate_solution(given_set):
    sol_length = random.randrange(2, len(given_set)+1)
    sol = {}
    for x in range(sol_length):
        random.randint(0, len(given_set))



def brute_force_solution(given_set):
    for x in range(1, len(given_set) + 1):
        subsets = set(combinations(given_set, x))
        for a_set in subsets:
            if sum(a_set) == 0: return set(a_set)


def goal_function(given_set, subset):
    """funkcja obliczająca jakość podanego rozwiązania"""
    if subset in given_set:
        return sum(subset)

    return None


if __name__ == '__main__':
    given_set = load_data("set2.json")
    print("Dany zbiór wejściowy: ", given_set)
    #
    # subset = generate_solution(given_set)
    #
    # print("Znalezione rozwiązanie: ", subset)

    generate_solution(given_set)
