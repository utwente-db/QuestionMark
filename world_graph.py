from itertools import combinations
import numpy

# Definition of a world graph from paper of TODO.


def set_all_offers(matching_graph):
    all_offers = []
    for offer_tuple in matching_graph.keys():
        if offer_tuple[0] not in all_offers:
            all_offers.append(offer_tuple[0])
        if offer_tuple[1] not in all_offers:
            all_offers.append(offer_tuple[1])
    return all_offers


def get_probabilities(possible_worlds, matching_graph):
    probabilities = []
    for possible_world in possible_worlds:
        world_probabilities = []
        for offer_tuple, probability in matching_graph.items():
            tuple_list = [offer_tuple[0], offer_tuple[1]]
            if probability == 1 or probability == 0:
                continue
            if tuple_list in possible_world:
                world_probabilities.append(probability)
            else:
                world_probabilities.append(1 - probability)
        probabilities.append(numpy.prod(world_probabilities))
    return probabilities


def get_consistent_graphs(possible_worlds):
    consistent_worlds = []
    transitive = True
    for world in possible_worlds:
        # Check transitivity
        if not transitive:
            continue
        for offer_a, offer_b in world:
            if not transitive:
                break
            for offer_c, offer_d in world:
                if (offer_b == offer_c) and ((offer_a, offer_d) not in world):
                    transitive = False
                    break
        consistent_worlds.append(world) if transitive else consistent_worlds.append([])
        transitive = True

    return consistent_worlds


def generate_possible_worlds(matching_graph):
    include_list = []
    combination_list = []
    for offer_tuple, probability in matching_graph.items():
        if probability == 1:
            include_list.append(sorted(offer_tuple))
        elif probability == 0:
            continue  # There is never an edge between this tuple in any possible world.
        else:
            combination_list.append(sorted(offer_tuple))
    possible_worlds = list()
    # Get all combinations from the uncertain edges and create the possible worlds.
    for n in range(1, len(combination_list) + 1):
        possible_worlds += list(combinations(combination_list, n))

    # Include the certain edge in each possible world.
    for offer_tuple in include_list:
        for world in possible_worlds:
            list(world).append(offer_tuple)

    # Generate the probabilities of the edges from a world-graph
    probabilities = get_probabilities(possible_worlds, matching_graph)

    # consistent_worlds can be empty when M-graph is not valid. Remove all inconsistent ones.
    consistent_worlds = get_consistent_graphs(possible_worlds)

    # normalise probabilities of remaining worlds.
    to_remove = []
    for i in range(len(consistent_worlds)):
        if not consistent_worlds[i]:
            to_remove.append(i)
    for i in sorted(to_remove, reverse=True):
        consistent_worlds.pop(i)
        probabilities.pop(i)
    prob_sum = 0
    for prob in probabilities:
        prob_sum += prob
    for i in range(len(probabilities)):
        probabilities[i] = probabilities[i] / prob_sum

    return consistent_worlds, probabilities


class WorldGraph:
    # M  = {}  # Matching graph. Dict with a tuple of offers as key and the probability of their edge as a value.
    N  = []  # all offers in the possible world. List of integers.
    Es = []  # the offers connected by an edge per consistent world. 2D List of tuples.
    Ps = []  # the probability of the possible world. List of Float.

    # The index of Es and Ps correspond to the same possible world.
    # Type of matching_graph: {(offer_id_1, offer_id_2): float, ...}

    def __init__(self, m):
        # self.M  = m,
        self.N  = set_all_offers(m)
        self.Es, self.Ps = generate_possible_worlds(m)

    def get_representation(self):
        return [self.N, self.Es, self.Ps]

    def get_n(self):
        return self.N

    def get_es(self):
        return self.Es