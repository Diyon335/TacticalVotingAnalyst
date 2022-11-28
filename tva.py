"""
The Tactical Voter Analyst (TVA) for the course: Multi-Agent Systems

@authors: Diyon Wickrameratne, Kaspar Kallast, Luca Forte, Lucas Padolevicius, Olmo Denegri

"""

import importlib
import random
import numpy as np

from agents.agent import Agent, get_winner


class TVA:
    """
    Tactical Voting Analyst class
    """

    def __init__(self, candidate_string, voting_scheme, num_agents):
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
            overall_happiness[happiness_computation] = sum(happinesses[happiness_computation])/len(happinesses[happiness_computation])

        return overall_happiness

    def get_report(self):
        """
        Creates a report of the entire election, and highlights the most important information
        :return: Returns a string reporting the important info of the election
        """

        string = ""

        string += "##### ELECTION RESULTS #####\n\n"
        string += f"Voting scheme: {self.voting_scheme}\n"

        agent_string = ""
        for a in self.agents:
            agent_string += str(a)+" "

        string += f"The voters: {agent_string}\n"

        string += f"The voters preferences are summarised below\n"
        string += str(self.get_preference_matrix())+"\n"

        string += f"Here are all the results\n"
        string += str(self.results)+"\n"
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

        string += f"The overall happiness is: {overall_happiness}"

        string += "\n"

        string += "############################"

        return string


def create_and_run_election(n_voters, n_candidates, voting_scheme):

    candidates = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    candidates = candidates[:n_candidates]

    election = TVA(candidates, voting_scheme, n_voters)
    election.run()
    election.get_report()   # not the best way do to this, but we need to run this function to properly
                            # update self.happinesses for overall happiness calculation, unless we just change
                            # this and somehow transfer overall happiness calculation into election.run()

    return election.get_overall_happiness(election.happinesses)


if __name__ == "__main__":

    candidates = "ABCDE"
    voting_scheme = "Plurality"
    voters = 5
    happiness_threshold = 99

    election = TVA(candidates, voting_scheme, voters)
    election.run()

    print(election.get_report())
    print("\n")

    print("##### TACTICAL VOTING #####")

    # Check how agents would change their votes depending on happiness
    for agent in election.get_agents():

        print(str(agent))
        print(f"Initial happiness: {agent.get_happiness(election.results)}")

        d = agent.get_happiness(election.results)
        if d["percentage_social_index"] > happiness_threshold:
            print(str(agent) + " was happy and didn't change their preferences\n")

        else:
            dictionary = election.scheme().tactical_options(agent, election)

            if len(dictionary) < 1:
                print(f"{str(agent)} was unhappy, but did not have any tactical voting strategy\n")
                continue

            '''
            TO DO fix the following: since now the dictionaries holding tactical options always have two keys (one per
            happiness computation strategy), the program never enters the if statement above and therefore never hits
            "continue"; fixing this would allow for tactical voting risk computation, since I cannot really think
            of a clever way to do it that is not just setting a variable "agents_with_tactical_options = 0" and
            just increasing it by 1 every time the continue statement above is not triggered
            '''

            print(f"For {str(agent)}, the tactical options are:")

            for key in dictionary:
                for option in dictionary[key]:
                    print(f"Type of happiness {key}: Option:{option} new preferences: {dictionary[key][option][0]} , "
                          f"new winner: {dictionary[key][option][1]}, "
                          f"new voting outcome: {dictionary[key][option][2]}, "
                          f"new happiness: {dictionary[key][option][3][key]}, "
                          f"new overall happiness: {dictionary[key][option][4][key]}")
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