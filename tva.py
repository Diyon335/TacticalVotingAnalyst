import importlib
from agents.agent import Agent

import numpy as np
import random

# def generate_preferences(candidates, voters):
#
#     pref_dict = {}
#
#     for voter in voters:
#         pref_dict[voter] = random.sample(candidates, len(candidates))
#
#     print(pref_dict)
#
#     preferences = []
#     preferences.append([key for key in pref_dict])
#     for col in range(len(candidates)):
#         preferences.append([pref_dict[key][col] for key in pref_dict])
#
#     return preferences
#
# def get_winner(preferences, strategy):
#
#     if strategy == "plurality":
#
#         tally = {}
#         for preferred_candidate in preferences[1]:
#             if preferred_candidate in tally:
#                 tally[preferred_candidate] += 1
#             else:
#                 tally[preferred_candidate] = 1
#
#     elif strategy == "plurality_two":
#
#         tally = {}
#         for row in (1, 2):
#             for preferred_candidate in preferences[row]:
#                 if preferred_candidate in tally:
#                     tally[preferred_candidate] += 1
#                 else:
#                     tally[preferred_candidate] = 1
#
#     elif strategy == "anti-plurality":
#
#         tally = {}
#         for row in range(len(preferences[1:-1])):
#             for preferred_candidate in preferences[1:-1][row]:
#                 if preferred_candidate in tally:
#                     tally[preferred_candidate] += 1
#                 else:
#                     tally[preferred_candidate] = 1
#
#     elif strategy == "borda":
#
#         tally = {}
#         for row in range(len(preferences[1:])):
#             for preferred_candidate in preferences[1:][row]:
#                 if preferred_candidate in tally:
#                     tally[preferred_candidate] += len(preferences[1:]) - row - 1
#                 else:
#                     tally[preferred_candidate] = len(preferences[1:]) - row - 1
#
#     print(tally)
#     best_candidate = get_best_candidate(tally)
#
#     return best_candidate
#
# def get_best_candidate(tally):
#
#     candidates = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#
#     best_candidate = None
#     best_score = 0
#     for key in tally:
#         if tally[key] > best_score:
#             best_score = tally[key]
#             best_candidate = key
#         elif tally[key] == best_score and candidates.index(key) < candidates.index(best_candidate):
#             best_score = tally[key]
#             best_candidate = key
#
#     return best_candidate
#
# def happiness_calculator(winner, preferences, strategy):
#
#     if strategy == "sum_squares":
#
#         individual_happiness = {}
#
#         for voter in preferences[0]:
#             i = 1
#             while True:
#                 if preferences[i][voter - 1] == winner:
#                     individual_happiness[voter] = np.square(len(preferences[1:]) - i)
#                     break
#                 i += 1
#
#         print(individual_happiness)
#         total_happiness = sum(individual_happiness[key] for key in individual_happiness)
#         print(total_happiness)
#
#         return individual_happiness, total_happiness
#
#     elif strategy == "avg_percentage":
#
#         individual_happiness = {}
#
#         for voter in preferences[0]:
#             i = 1
#             while True:
#                 if preferences[i][voter - 1] == winner:
#                     individual_happiness[voter] = (len(preferences[1:]) - i)/(len(preferences[1:]) - 1)
#                     break
#                 i += 1
#
#         print(individual_happiness)
#         avg_happiness = sum(individual_happiness[key] for key in individual_happiness)/len(individual_happiness)
#         print(avg_happiness)
#
#         return individual_happiness, avg_happiness
#

# candidates = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# cand_number = 10
# voter_num = 10
# preferences = generate_preferences([char for char in candidates[:cand_number]], [i for i in range(1, voter_num + 1)])
# # pref = [[1, 2, 3, 4], ["A", "B", "C", "D"], ["A", "B", "C", "D"], ["A", "B", "C", "D"], ["A", "B", "C", "D"]]
# for row in preferences:
#     print(row)
# print()
# winner = get_winner(preferences, "borda")
# print(winner)
# print()
# happiness_calculator(winner, preferences, "sum_squares")


def main():
    """
    This is the main function of the TVA. You can update the candidates and voting scheme here. Agents can be
    manually created with their preferences and running the programme will apply the scheme

    :return: void
    """

    candidate_string = "ABCD"
    voting_scheme = "Plurality"

    module = importlib.import_module("voting.voting_schemes")

    # Check if module has the voting scheme
    if not hasattr(module, voting_scheme):
        raise Exception(f"{voting_scheme} has not been implemented")

    scheme = getattr(module, voting_scheme)

    candidates = {}

    for letter in candidate_string:
        candidates[letter] = 0

    # TODO find a way to handle preference that is not in candidate list, for example "Z"
    agent1 = Agent("Diyon", "BCDA", scheme)
    agent2 = Agent("Mike", "BACD", scheme)

    print(scheme().run_scheme(candidates, [agent1, agent2]))


if __name__ == "__main__":
    main()
