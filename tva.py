import importlib
from agents.agent import Agent


def main():
    """
    This is the main function of the TVA. You can update the candidates and voting scheme here. Agents can be
    manually created with their preferences and running the programme will apply the scheme

    :return: void
    """

    candidate_string = "ABCD"
    voting_scheme = "Plurality"

    module = importlib.import_module("voting.voting_schemes")

    # Check if module has the voting scheme
    if not hasattr(module, voting_scheme):
        raise Exception(f"{voting_scheme} has not been implemented")

    scheme = getattr(module, voting_scheme)

    candidates = {}

    for letter in candidate_string:
        candidates[letter] = 0

    agent1 = Agent("Diyon", "BCDA", scheme, candidates)
    agent2 = Agent("Mike", "ACDB", scheme, candidates)

    results = scheme().run_scheme(candidates, [agent1, agent2])

    agent1.get_happiness(results)


if __name__ == "__main__":
    main()
