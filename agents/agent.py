class Agent:
    """
    Class for an agent
    """

    def __init__(self, name, preference_string, voting_scheme):
        """
        Constructor for an agent

        :param name: A string for the name of the agent
        :param preference_string: A string indicating the preferences in order
        :param voting_scheme: A voting scheme object (Borda, Plurality, etc.)
        """

        self.name = name

        self.preferences = {}

        for preference in preference_string:
            self.preferences[preference] = 0

        voting_scheme().tally_personal_votes(self.preferences)

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

    def get_happiness(self, winner):
        """
        Computes happiness of an agent
        :param: winner: A string of one character indicating the winner of the election
        # TODO TO BE DONE, RIGHT NOW RETURNS 1 WAY
        :return: Returns a tuple of integers, representing the agent's happiness in different ways
        """

        pref_list = list(self.preferences.keys())
        index = pref_list.index(winner)

        return ((len(pref_list) - index - 1)/(len(pref_list) - 1)) * 100
