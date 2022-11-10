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

        # TODO implement happiness as it belongs to an agent

    def get_preferences(self):
        """
        Gets the tallied preferences of the agent

        :return: A dictionary with the tallied preferences of the agent
        """
        return self.preferences
