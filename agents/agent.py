class Agent:
    """
    Class for an agent
    """

    def __init__(self, name, preference_string, voting_scheme, candidates):
        """
        Constructor for an agent

        :param name: A string for the name of the agent
        :param preference_string: A string indicating the preferences in order
        :param voting_scheme: A voting scheme object (Borda, Plurality, etc.)
        :param candidates: A dictionary of all the candidates
        """

        self.name = name

        if len(preference_string) != len(candidates):
            raise Exception(f"Length of {self.name}'s preference is not equal to the amount of candidates")

        for pref in preference_string:
            if pref not in candidates:
                raise Exception(f"{self.name} entered an invalid preference")

        self.preferences = {}

        for preference in preference_string:
            self.preferences[preference] = 0

        voting_scheme().tally_personal_votes(self.preferences)

        self.happiness = 0

    def __str__(self):
        """
        String representation of an agent will be their name

        :return: Returns a string indicating the name of the agent
        """
        return self.name

    def get_preferences(self):
        """
        Gets the tallied preferences of the agent

        :return: A dictionary with the tallied preferences of the agent
        """
        return self.preferences

    def get_happiness(self, candidate_results):
        # TODO complete function description
        """
        Computes happiness of an agent in several different ways, namely:
        -
        -
        :param candidate_results: A dictionary of candidates after voting results have been cast
        :return: Returns a tuple of integers, representing the agent's happiness in different ways
        """

        sorted_results = dict(sorted(candidate_results.items(), key=lambda k: k[1], reverse=True))

        pass

    # TODO implement this stuff in here. Maybe return a tuple containing the different ways of happiness values
    # TODO for example: return (happiness_avg_percentage, happiness_sum_squares)
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

