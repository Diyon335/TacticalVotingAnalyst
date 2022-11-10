from abc import ABC, abstractmethod


class VotingScheme(ABC):
    """
    Abstract class voting scheme
    """

    def run_scheme(self, candidates, agents):
        """
        This function tallies the overall votes for all the candidates, based on the agents' preferences

        :param candidates: A dictionary of the candidates in the election
        :param agents: A list of agents who are voting
        :return: Returns a dictionary of the tallied votes for each candidate
        """
        candidate_dict = candidates

        for agent in agents:

            preference_dict = agent.get_preferences()

            for key in preference_dict:
                candidate_dict[key] += preference_dict[key]

        return candidate_dict

    @abstractmethod
    def tally_personal_votes(self, preferences):
        """
        Abstract method for the voting schemes. Requires a dictionary of personal preferences from an agent
        It modifies the preference dictionary of a user

        :param preferences: A dictionary of an agent's preferences
        :return: void
        """
        pass


class Borda(VotingScheme):
    """
    Borda voting class

    Borda voting tallies votes in a way where, an agent's preference receive a score of m - i, where "m"
    is the number of candidates, and "i" is the position of the preference in their preference list

    For example, "A" would receive a score of 3-1 = 2, if the preferences of the agent were ACB, and the candidates
    were ABC
    """

    def tally_personal_votes(self, preferences):
        pass


class Plurality(VotingScheme):
    """
    Plurality voting class

    The agents highest preference gets a score of 1
    """

    def tally_personal_votes(self, preferences):

        first_preference = next(iter(preferences))
        preferences[first_preference] += 1
