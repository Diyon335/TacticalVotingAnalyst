"""
The Tactical Voter Analyst (TVA) for the course: Multi-Agent Systems

@authors: Diyon Wickrameratne, Kaspar Kallast, Luca Forte, Lucas Padolevicius, Olmo Denegri

"""

import importlib
import random
import numpy as np

from agents.agent import Agent


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

    def run(self):
        """
        A void function to run the selected voting scheme

        :return: void
        """
        self.results = self.scheme().run_scheme(self.candidates, self.agents)

    def get_winner(self, results=None):
        """
        Returns the winning candidate. In the case of a tie, the winner will be chosen alphabetically (i.e., the agent
        whose name begins with the lowest letter in the alphabet)

        :return: A string with one character indicating the winner
        """

        winner = ""
        max_votes = 0

        if results is None:
            results = self.results

        for candidate in results:
            if results[candidate] > max_votes:
                winner = candidate
                max_votes = results[candidate]

            elif results[candidate] < max_votes:
                continue

            else:
                if candidate < winner:
                    winner = candidate

        return winner

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
        string += f"The winner of this election is: {self.get_winner()}\n"

        string += "The happiness of all agents are:\n"

        for a in self.agents:
            string += f"{a.name} : {a.get_happiness(self.get_winner())} %\n"

        string += "\n"

        string += "############################"

        return string


if __name__ == "__main__":

    candidates = "ABCDEFGHI"
    voting = "Plurality"
    voters = 10
    happiness_threshold = 80

    election = TVA(candidates, voting, voters)
    election.run()

    print(election.get_report())
    print("\n")

    print("##### TACTICAL VOTING #####")

    # Check how agents would change their votes depending on happiness
    for agent in election.get_agents():

        print(str(agent))
        print(f"Initial happiness: {agent.get_happiness(election.get_winner())}")

        if agent.get_happiness(election.get_winner()) > happiness_threshold:
            print(str(agent) + " was happy and didn't change their preferences\n")

        else:
            dictionary = election.scheme().tactical_options(agent, election)

            if len(dictionary) < 1:
                print(f"{str(agent)} was unhappy, but did not have any tactical voting strategy\n")
                continue

            print(f"For {str(agent)}, the tactical options are:")

            for key in dictionary:
                print(f"Option {key}: new preferences: {dictionary[key][0]} , new winner: {dictionary[key][1]}, "
                      f"new happiness: {dictionary[key][2]}")
            print("\n")
