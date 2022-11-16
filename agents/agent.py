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

        self.tactical_preferences = {}

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

    def vote_tactical(self, winner, voting_scheme):
        """
        Depending on the voting scheme, the agent can vote tactically and change its tactical preference dictionary

        If an agent's first choice is the winner, they won't change their voting strategy

        :param winner: A string with one character indicating the winner of the election
        :param voting_scheme: A voting scheme object
        :return: void
        """
        first_pref = next(iter(self.preferences))

        if winner != first_pref:
            voting_scheme().tactical_options(winner, self.preferences, self.tactical_preferences)

    def get_tactical_preferences(self):
        """
        Gets the newly tallied tactical preferences of the agent
        :return: A dictionary with the newly tallied preferences of the agent
        """
        return self.tactical_preferences

    def get_preferences(self):
        """
        Gets the tallied preferences of the agent

        :return: A dictionary with the tallied preferences of the agent
        """
        return self.preferences

    def get_happiness(self, winner):
        """
        Computes happiness of an agent in several different ways, namely:
        :param: winner: A string of one character indicating the winner of the election
        :return: Returns a tuple of integers, representing the agent's happiness in different ways
        """

        pref_list = list(self.preferences.keys())
        index = pref_list.index(winner)

        return ((len(pref_list) - index - 1)/(len(pref_list) - 1)) * 100
