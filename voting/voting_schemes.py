from abc import ABC, abstractmethod
from copy import copy


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

    @abstractmethod
    def tactical_options(self, agent, tva_object):
        """
        Abstract function to change an agent's order of votes, depending on the winner. For each voting strategy, the
        agent is able to tactically change their votes to increase happiness. This function returns a dictionary
        containing all tactical options for a given voting strategy.

        The dictionary follows the structure:
        # TODO TO BE DECIDED. FOR NOW IT'S:
        # TODO <key> : <value>, where key = option number, and value is a list with three indices
        # TODO index 1 = new voting preference list
        # TODO index 2 = new winner because of this agent's new preference list
        # TODO index 3 = new happiness after subsequent re-election

        :param tva_object: A TVA object
        :param agent: The agent object for which tactical voting must be applied
        :return: Returns a dictionary of several tactical voting strategies the agent can apply
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

    def tactical_options(self, agent, tva_object):
        pass

    def tally_personal_votes(self, preferences):

        m = len(preferences)
        i = 1
        for key in preferences:
            preferences[key] = m - i
            i += 1


class Plurality(VotingScheme):
    """
    Plurality voting class

    The agents highest preference gets a score of 1
    """

    def tally_personal_votes(self, preferences):

        first_preference = next(iter(preferences))
        preferences[first_preference] += 1

    def tactical_options(self, agent, tva_object):

        tactical_set = {}

        total_agents = len(tva_object.get_agents())

        winner = tva_object.get_winner()

        # If more than half agents voted for the winning candidate, there is no tactical voting strategy for the
        # current agent
        if not tva_object.results[winner] > (total_agents/2):

            original_list = list(agent.preferences)
            stop_index = original_list.index(winner)

            for i in range(1, stop_index):

                new_list = copy(original_list)
                temp = new_list[i]
                new_list[i] = new_list[0]
                new_list[0] = temp

                results_copy = tva_object.results
                # Our original vote is taken away from the results
                results_copy[original_list[0]] -= 1

                # We add one vote to the candidate that we switch
                results_copy[original_list[i]] += 1

                new_winner = tva_object.get_winner(results=results_copy)

                if new_winner != winner:
                    # TODO ASK GERARD ABOUT NEW_WINNER (VALUE OR WHOLE?)
                    # TODO IMPLEMENT OVERALL HAPPINESS
                    tactical_set[i] = [new_list, new_winner, agent.get_happiness(new_winner)]

        return tactical_set


class AntiPlurality(VotingScheme):
    """
    Anti-plurality voting class

    The agent's lowest preference gets a score of 0, while others get 1
    """
    def tally_personal_votes(self, preferences):

        i = 0
        for key in preferences:

            if i < len(preferences) - 1:
                preferences[key] += 1

            i += 1

    def tactical_options(self, agent, tva_object):
        pass


class VotingForTwo(VotingScheme):
    """
    Voting for two

    First and second choice get a score of 1
    """
    def tally_personal_votes(self, preferences):

        iterable = iter(preferences)

        preference = next(iterable)
        preferences[preference] += 1
        preference = next(iterable)
        preferences[preference] += 1

    def tactical_options(self, agent, tva_object):
        pass
