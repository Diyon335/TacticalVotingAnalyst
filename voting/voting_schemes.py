from abc import ABC, abstractmethod
from copy import copy, deepcopy
from agents.agent import get_winner

'''
TO DO: move this anywhere else where it makes sense, for now it's here just for convenience sake
'''


def get_tactical_overall_happiness(tva_object, agent, agent_happiness, results_copy):

    happinesses = {}

    for other_agent in tva_object.get_agents():
        if other_agent != agent:
            other_happiness = other_agent.get_happiness(results_copy)
            for key in other_happiness:
                if key not in happinesses:
                    happinesses[key] = []
                happinesses[key].append(other_happiness[key])
        else:
            for key in agent_happiness:
                if key not in happinesses:
                    happinesses[key] = []
                happinesses[key].append(agent_happiness[key])

    for key in happinesses:
        happinesses[key] = sum(happinesses[key])/len(happinesses[key])

    return happinesses


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
        candidate_dict = copy(candidates)

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

        tactical_set = {"percentage_my_preference": {}, "percentage_social_index": {}}

        """
        For percentage_my_preference
        """

        total_agents = len(tva_object.get_agents())

        winner = get_winner(tva_object.results)

        # If more than half agents voted for the winning candidate, there is no tactical voting strategy for the
        # current agent
        if not tva_object.results[winner] > (total_agents/2):

            original_list = list(agent.preferences)
            stop_index = original_list.index(winner)

            for i in range(1, stop_index):

                new_pref_list = copy(original_list)
                temp = new_pref_list[i]
                new_pref_list[i] = new_pref_list[0]
                new_pref_list[0] = temp

                results_copy = copy(tva_object.results)
                # Our original vote is taken away from the results
                results_copy[original_list[0]] -= 1

                # We add one vote to the candidate that we switch
                results_copy[original_list[i]] += 1

                new_winner = get_winner(results_copy)

                if new_winner != winner:

                    agent_happiness = agent.get_happiness(results_copy)
                    new_overall_happiness = get_tactical_overall_happiness(tva_object, agent,
                                                                           agent_happiness, results_copy)

                    tactical_set["percentage_my_preference"][i] = [new_pref_list, new_winner,
                                                                   results_copy, agent_happiness,
                                                                   new_overall_happiness]

        """
        For percentage_social_index
        """

        # Not possible

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

        tactical_set = {"percentage_my_preference": {}, "percentage_social_index": {}}

        """
        For percentage_my_preference
        """

        winner = get_winner(tva_object.results)
        original_list = list(agent.preferences)
        winner_index = original_list.index(winner)

        # if the winner is not already in the last position I can investigate if I have a
        # tactical voting option
        if original_list[-1] != winner:

            new_pref_list = copy(original_list)
            temp = new_pref_list[-1]
            new_pref_list[-1] = winner
            new_pref_list[winner_index] = temp

            results_copy = copy(tva_object.results)
            results_copy[original_list[-1]] += 1
            results_copy[original_list[winner_index]] -= 1

            new_winner = get_winner(results_copy)

            if new_winner != winner:

                agent_happiness = agent.get_happiness(results_copy)
                new_overall_happiness = get_tactical_overall_happiness(tva_object, agent,
                                                                       agent_happiness, results_copy)

                tactical_set["percentage_my_preference"][0] = [new_pref_list, new_winner,
                                                               results_copy, agent_happiness,
                                                               new_overall_happiness]

        """
        For percentage_social_index
        """
        pref_dict = copy(agent.get_preferences())
        pref_list = list(pref_dict.keys())

        least_preferred = pref_list[-1]

        results_copy = copy(tva_object.results)
        results_copy[least_preferred] += 1

        original_happiness = agent.get_happiness(tva_object.results)

        if results_copy[least_preferred] > results_copy[pref_list[0]]:

            tactical_set["percentage_social_index"] = {}

        elif results_copy[least_preferred] == results_copy[pref_list[0]] and least_preferred < pref_list[0]:

            tactical_set["percentage_social_index"] = {}

        else:

            results_copy = copy(tva_object.results)
            results_list = sorted(results_copy, key=lambda k: results_copy[k], reverse=True)

            stop_index = results_list.index(pref_list[0])

            for i in range(0, stop_index):

                list_copy = copy(pref_list)

                temp_i = results_list[i]
                temp_last = pref_list[-1]

                list_copy[pref_list.index(temp_i)] = temp_last
                list_copy[-1] = temp_i

                '''
                ### TO DO: can we remove deepcopy from here? because deepcopy is super slow
                '''
                agent_copy = copy(agent)

                new_prefs = {}
                for candidate in list_copy:
                    new_prefs[candidate] = 0

                self.tally_personal_votes(new_prefs)
                agent_copy.preferences = new_prefs

                new_agents = [agent_copy]

                for a in tva_object.get_agents():
                    if not a == agent:
                        new_agents.append(a)

                new_results = self.run_scheme(tva_object.candidates, new_agents)
                new_winner = get_winner(new_results)

                new_happiness = agent.get_happiness(new_results)

                if new_happiness["percentage_social_index"] <= original_happiness["percentage_social_index"]:
                    continue

                tactical_set["percentage_social_index"][i] = [list_copy, new_winner, new_happiness]

        return tactical_set


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

        tactical_set = {"percentage_my_preference": {}, "percentage_social_index": {}}

        """
        For percentage_my_preference
        """

        winner = get_winner(tva_object.results)
        original_list = list(agent.preferences)
        winner_index = original_list.index(winner)

        # if the winner is not in the third position of my preference order I can investigate
        # if I have tactical voting options
        if winner_index != 2:

            if winner_index == 1:

                for i in range(2, len(original_list)):

                    new_pref_list = copy(original_list)
                    temp = new_pref_list[i]
                    new_pref_list[i] = winner
                    new_pref_list[1] = temp

                    results_copy = copy(tva_object.results)
                    results_copy[original_list[1]] -= 1
                    results_copy[original_list[i]] += 1

                    new_winner = get_winner(results_copy)

                    if new_winner == original_list[0]:

                        agent_happiness = agent.get_happiness(results_copy)
                        new_overall_happiness = get_tactical_overall_happiness(tva_object, agent,
                                                                               agent_happiness, results_copy)

                        tactical_set["percentage_my_preference"][i - 2] = [new_pref_list, new_winner,
                                                                           results_copy, agent_happiness,
                                                                           new_overall_happiness]

            else:

                for i in range(2, winner_index):

                    new_pref_list = copy(original_list)
                    temp = new_pref_list[i]
                    new_pref_list[i] = new_pref_list[1]
                    new_pref_list[1] = temp

                    results_copy = copy(tva_object.results)
                    results_copy[original_list[i]] += 1
                    results_copy[original_list[1]] -= 1

                    new_winner = get_winner(results_copy)

                    if original_list.index(new_winner) < winner_index:

                        agent_happiness = agent.get_happiness(results_copy)
                        new_overall_happiness = get_tactical_overall_happiness(tva_object, agent,
                                                                               agent_happiness, results_copy)

                        tactical_set["percentage_my_preference"][i - 2] = [new_pref_list, new_winner,
                                                                           results_copy, agent_happiness,
                                                                           new_overall_happiness]

        """
        For percentage_social_index
        """
        pref_dict = copy(agent.get_preferences())
        pref_list = list(pref_dict.keys())

        first_pref = pref_list[0]
        second_pref = pref_list[1]

        original_happiness = agent.get_happiness(tva_object.results)

        results_dict = copy(tva_object.results)

        if not results_dict[second_pref] - results_dict[first_pref] >= 2 or \
                (results_dict[second_pref] - results_dict[first_pref] == 1 and second_pref < first_pref):

            for i in range(2, len(pref_list)):

                results_dict_copy = copy(results_dict)

                results_dict_copy[pref_list[i]] += 1

                if results_dict_copy[pref_list[i]] > results_dict_copy[first_pref] and pref_list[i] < first_pref:
                    results_dict_copy[pref_list[i]] -= 1
                    continue

                else:

                    results_dict_copy[pref_list[i]] -= 1

                    pref_list_copy = copy(pref_list)

                    temp = pref_list_copy[i]
                    pref_list_copy[i] = second_pref
                    pref_list_copy[1] = temp

                    new_pref_dict = {}
                    for element in pref_list_copy:
                        new_pref_dict[element] = 0

                    self.tally_personal_votes(new_pref_dict)
                    agent_copy = copy(agent)
                    agent_copy.preferences = new_pref_dict

                    new_agents = [agent_copy]

                    for a in tva_object.get_agents():
                        if not a == agent:
                            new_agents.append(a)

                    new_results = self.run_scheme(tva_object.candidates, new_agents)
                    new_winner = get_winner(new_results)

                    new_happiness = agent.get_happiness(new_results)

                    if new_happiness["percentage_social_index"] <= original_happiness["percentage_social_index"]:
                        continue

                    new_overall_happiness = get_tactical_overall_happiness(tva_object, agent, new_happiness, new_results)

                    tactical_set["percentage_social_index"][i] = [pref_list_copy, new_winner, new_results,
                                                                  new_happiness, new_overall_happiness]

        return tactical_set