"""
The Tactical Voter Analyst (TVA) for the course: Multi-Agent Systems

@authors: Diyon Wickrameratne, Kaspar Kallast, Luca Forte, Lucas Padolevicius, Olmo Denegri

"""

import importlib
import random
import numpy as np
from copy import copy

from agents.agent import Agent, get_winner


class TVA:
    """
    Tactical Voting Analyst class
    """

    def __init__(self, candidate_string, voting_scheme, num_agents, advanced_tva):
        """
        The constructor for the TVA

        When initialised, this constructor creates a dictionary of the candidates from the candidate string.
        The class then imports the respective voting scheme - raises an exception if not found in voting_schemes.py
        It also creates the specified number of agents

        :param candidate_string: A string of candidates, for example: "ABCDEFG"
        :param voting_scheme: A string indicating the type of voting
        :param num_agents: An integer for the number of agents in the election
        """

        self.candidate_string = candidate_string
        self.candidates = self.create_candidates()
        self.num_agents = num_agents
        self.voting_scheme = voting_scheme
        self.is_atva = advanced_tva

        module = importlib.import_module("voting.voting_schemes")

        # Check if module has the voting scheme
        if not hasattr(module, voting_scheme):
            raise Exception(f"{voting_scheme} has not been implemented")

        self.scheme = getattr(module, voting_scheme)

        self.agents = self.create_agents(num_agents)

        self.results = {}

        self.happinesses = {}

    def run(self):
        """
        A void function to run the selected voting scheme

        :return: void
        """
        self.results = self.scheme().run_scheme(self.candidates, self.agents)

    def get_agents(self):
        """
        :return: Returns a list of agent objects in the election
        """
        return self.agents

    def create_agents(self, num_agents):
        """
        Creates a specified number of agents

        :param num_agents: An integer indicating the number of agents to create
        :return: Returns a list of agent objects
        """
        agents = []

        for i in range(num_agents):
            agents.append(Agent(f"Agent{i + 1}", self.generate_preferences(), self.scheme))

        return agents

    def generate_preferences(self):
        """
        Generates a randomly shuffled string from the candidate string. This is used to generate random
        agent preferences

        :return: Returns a randomly shuffled string
        """
        return "".join(random.sample(self.candidate_string, len(self.candidate_string)))

    def create_candidates(self):
        """
        Creates a dictionary of the candidates in the election. It initially sets all votes to 0

        :return: Returns a dictionary of the candidates, will all their votes set to 0
        """

        candidate_dict = {}

        for letter in self.candidate_string:
            candidate_dict[letter] = 0

        return candidate_dict

    def get_preference_matrix(self):
        """
        Creates a matrix representation of all agents' preferences. Each column in the matrix represents the
        preferences of an agent, in preference order

        :return: Returns a nested list (or matrix) representing all preferences of all agents
        """

        matrix = []

        for agent in self.agents:

            row = [agent.name]

            for candidate in agent.get_preferences():
                row.append(f"{candidate}")

            matrix.append(row)

        np_matrix = np.array(matrix)

        return np_matrix.transpose()

    def get_overall_happiness(self, happinesses):

        overall_happiness = {}

        for happiness_computation in happinesses:
            overall_happiness[happiness_computation] = sum(happinesses[happiness_computation]) / len(
                happinesses[happiness_computation])

        return overall_happiness

    def get_report(self):
        """
        Creates a report of the entire election, and highlights the most important information
        :return: Returns a string reporting the important info of the election
        """

        string = ""

        preference_happiness_count = 0
        social_index_count = 0

        string += "##### ELECTION RESULTS #####\n\n"
        string += f"Voting scheme: {self.voting_scheme}\n"

        agent_string = ""
        for a in self.agents:
            agent_string += str(a) + " "

        string += f"The voters: {agent_string}\n"

        string += f"The voters preferences are summarised below\n"
        string += str(self.get_preference_matrix()) + "\n"

        string += f"Here are all the results\n"
        string += str(self.results) + "\n"
        string += f"The winner of this election is: {get_winner(self.results)}\n"

        string += "The happiness of all agents are:\n"

        for a in self.agents:
            happiness = a.get_happiness(self.results)
            string += f"{a.name} : {happiness} %\n"

            for happiness_computation in happiness:
                if happiness_computation not in self.happinesses:
                    self.happinesses[happiness_computation] = []
                self.happinesses[happiness_computation].append(happiness[happiness_computation])

        overall_happiness = self.get_overall_happiness(self.happinesses)

        string += f"The overall happiness is: {overall_happiness}\n\n"

        string += "##### TACTICAL VOTING #####\n\n"

        # Check how agents would change their votes depending on happiness
        for a in self.agents:

            happiness_dict = a.get_happiness(self.results)

            string += f"For {str(a)} with initial happiness: {happiness_dict}\n"

            if happiness_dict["percentage_social_index"] > happiness_threshold and \
                    happiness_dict["percentage_my_preference"] > happiness_threshold:

                string += f"{str(a)} was happy and didn't change their preferences\n\n"

            else:
                tact_dictionary = self.scheme().tactical_options(a, election)

                string += f"For {str(a)}, the tactical options are:\n"

                for key in tact_dictionary:

                    if len(tact_dictionary[key]) < 1:
                        string += f"{str(a)} was unhappy ({key}), but did not have any tactical voting strategy\n\n"
                        continue

                    if key == "percentage_my_preference":
                        preference_happiness_count += 1

                    if key == "percentage_social_index":
                        social_index_count += 1

                    for option in tact_dictionary[key]:
                        string += f"Type of happiness {key}: Option:{option} new preferences: {tact_dictionary[key][option][0]} , " \
                                  f"new winner: {tact_dictionary[key][option][1]}, " \
                                  f"new voting outcome: {tact_dictionary[key][option][2]}, " \
                                  f"new happiness: {tact_dictionary[key][option][3][key]}, " \
                                  f"new overall {key} happiness: {tact_dictionary[key][option][4][key]}\n"

            string += "------------------------\n"

        string += f"Risk based on preference happiness: {preference_happiness_count / len(self.agents)}\n"
        string += f"Risk based on social index happiness: {social_index_count / len(self.agents)}\n\n"

        if self.is_atva:

            string += f"##### ADVANCED TVA: Counter voting strategies #####\n\n"

            for a in self.agents:

                counter_voting_set = self.scheme().counter_vote(a, copy(self))

                string += f"For {str(a)} \n"

                # element is a list = [other_agent, their prefs (list), new results (list),
                # tactical options of agent after the other agents prefs (dict)]
                for happiness_type in counter_voting_set:
                    string += f"\tConsidering {happiness_type}:\n\n"

                    for sublist in counter_voting_set[happiness_type]:

                        other_agent = sublist[0]
                        other_prefs = sublist[1]
                        new_results = sublist[2]
                        new_tact_options = sublist[3]

                        if other_prefs is None:
                            string += f"\t{other_agent} didn't have any tactical voting strategies, so {a} isn't affected\n"
                            string += "--------------------------\n"
                            continue

                        string += f"\tFor the type of happiness: {happiness_type}\n"
                        string += f"\tIf {str(other_agent)} decides to go with new preferences: {other_prefs}\n"
                        string += f"\tThe new results would be: {new_results}\n"

                        if len(new_tact_options) < 1:
                            string += f"\tBut {str(a)} would not have any tactical options for this counter\n"
                            string += "--------------------------\n"
                            continue

                        string += f"\tTherefore, {str(a)} has these tactical options:\n"

                        for option in new_tact_options:
                            string += f"\tType of happiness {happiness_type}: Option:{option} new preferences: {new_tact_options[option][0]} , " \
                                      f"new winner: {new_tact_options[option][1]}, " \
                                      f"new voting outcome: {new_tact_options[option][2]}, " \
                                     f"new happiness: {new_tact_options[option][3][happiness_type]}, " \
                                     f"new overall {happiness_type} happiness: {new_tact_options[option][4][happiness_type]}\n"
                        string += "--------------------------\n"

            string += f"##### ADVANCED TVA: Concurrent voting strategies #####\n\n"

            new_social_outcomes = self.scheme().concurrent_vote(copy(self))

            for happiness_type in new_social_outcomes:

                string += f"For {happiness_type}, the new social outcome if all agents voted concurrently:\n"

                winner = new_social_outcomes[happiness_type][0]
                string += f"The new winner is: {winner} if the following agents voted:\n"

                for i in range(1, len(new_social_outcomes[happiness_type])):
                    nested_list = new_social_outcomes[happiness_type][i]

                    string += f"{nested_list[0]}: {nested_list[1]}, is original: {nested_list[2]}\n"

        return string


def create_and_run_election(n_voters, n_candidates, voting_scheme):
    candidates = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    candidates = candidates[:n_candidates]

    election = TVA(candidates, voting_scheme, n_voters)
    election.run()
    election.get_report()  # not the best way do to this, but we need to run this function to properly
    # update self.happinesses for overall happiness calculation, unless we just change
    # this and somehow transfer overall happiness calculation into election.run()

    return election.get_overall_happiness(election.happinesses)


if __name__ == "__main__":

    candidates = "ABCDEFGHIJK"
    voting_scheme = "Plurality"
    voters = 5
    show_atva_features = True
    happiness_threshold = 99

    election = TVA(candidates, voting_scheme, voters, show_atva_features)
    election.run()

    print(election.get_report())
    print("\n")

    '''tests = 1000
    total_overall_happiness = {"percentage_my_preference": 0, "percentage_social_index": 0}
    n_voters = 25
    n_candidates = 8
    voting_scheme = "Plurality"

    for i in range(tests):

        new_overall_happiness = create_and_run_election(n_voters, n_candidates, voting_scheme)
        for key in new_overall_happiness:
            total_overall_happiness[key] += new_overall_happiness[key]

    average_overall_happiness = {}
    for key in total_overall_happiness:
        average_overall_happiness[key] = total_overall_happiness[key]/tests
    print(average_overall_happiness)'''
