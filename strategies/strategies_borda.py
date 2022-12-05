import operator

import voting.voting_schemes as vs
import agents.agent as ag

class Strategies_borda:
    """
    Class for a Borda voting strategy
    """

    def __init__(self, voting_scheme):
        """
        Constructor for the Borda voting strategy

        :param voting_scheme: voting scheme used
        """
        valid = False
        if voting_scheme == "Borda":
            valid = True

        if not valid:
            print("Error: unsupported voting and happiness scheme combination.")
        # self.votes = {
        #             "A":7,
        #             "B":8,
        #             "C":6,
        #             "D":9 }

    def check_if_best(self, agent, votes):
        """
        Checks if an agent can change voting strategy to find a better outcome

        :param agent: the agent changing their voting strategy
        :param votes: dict of all candidates with corresponding tallied votes
        :return possible: Boolean of whether the candidate can be in 1st place
        :return pref: dict of agent preferences, updated if (possible = True) to make it do so
        """
        winner = max(votes, key=votes.get)
        #print("votes are ",votes)

        ## Clear votes
        new_votes = votes.copy()
        prefs = agent.get_preferences()
        le = len(prefs)
        for cand in prefs:
            le -= 1
            new_votes[cand] -= le
        #print("new votes are ",new_votes)
        #print("prefs are ",prefs)
        for x in prefs:
            if x == winner:
                #print("x is a winner")
                return [False, {}]
            [possible, pref] = self.check_winner_possible(x, prefs, new_votes)
            if possible:
                return [possible, pref]
        #print("no better opts")
        return [False, {}]

    def check_winner_possible(self, candidate, prefs, votes):
        """
        Checks if an agent can change voting strategy to make a specific candidate win

        :param candidate: the candidate to get to 1st place
        :param prefs: preference dict of the agent changing their voting strategy
        :return possible: Boolean of whether the candidate can be in 1st place
        :return pref: agent preferences, updated if (possible = True) to make it do so
        """
        new_prefs = {}
        #print(prefs)
        #print(votes)
        up_bound = votes[candidate]+(len(prefs)-1)
        new_prefs[candidate] = len(prefs)-1
        #print(new_prefs)
        res = {}
        for x in prefs:
            if x != candidate:
                # if our wanted winner wins the tie, x can get up to the same score
                if candidate < x:
                    diff = up_bound - votes[x]
                    if(diff < 0):
                        return [False, {}]
                    res.update({x:diff})
                # if our wanted winner loses the tie, x can get up to 1 below the same score
                else:
                    diff = up_bound - votes[x] - 1
                    if(diff < 0):
                        return [False, {}]
                    res.update({x:diff})
                #print("interim: ",res)

        for x in range(len(prefs)-2,-1,-1):
            maxi = max(res, key=res.get)
            if(x > res[maxi]):
                #print("max was:",res[maxi])
                return [False, {}]
            new_prefs.update({maxi:x})
            res.pop(maxi)
            #print("new prefs: ",new_prefs)
            #print()
        #print("final preferences: ",new_prefs)
        return [True, new_prefs]


# ab = Strategies_borda(vs.Borda())
# agent = ag.Agent("you", "ABCD", vs.Borda())
# ab.check_if_best(agent,ab.votes)

