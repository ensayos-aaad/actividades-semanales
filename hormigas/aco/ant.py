import random
import csv
import math
# The Ant class encompasses the idea of an ant in the ACO algorithm.
# Ants will move to different attractions and leave pheromones behind. Ants will also make a judgement about which
# attraction to visit next. And lastly, ants will have knowledge about their respective total distance travelled.
# - Memory: In the ACO algorithm, this is the list of attractions already visited.
# - Best fitness: The shortest total distance travelled across all attractions.
# - Action: Choose the next destination to visit and drop pheromones along the way.
class Ant:

    # Variables de clase
    ATTRACTION_COUNT = 0
    RANDOM_ATTRACTION_FACTOR = 0
    ALPHA = 4 # Set the weight for pheromones on path for selection
    BETA = 7  # Set the weight for heuristic of path for selection
    attraction_distances = []

    # The ant is initialized to a random attraction with no previously visited attractions
    def __init__(self):
        self.visited_attractions = []
        self.visited_attractions.append(random.randint(0, self.ATTRACTION_COUNT - 1))

    # Select an attraction using a random chance or ACO function
    def visit_attraction(self, pheromone_trails):
        if random.random() < self.RANDOM_ATTRACTION_FACTOR:
            self.visited_attractions.append(self.visit_random_attraction())
        else:
            self.visited_attractions.append(
                self.roulette_wheel_selection(self.visit_probabilistic_attraction(pheromone_trails)))

    # Select an attraction using a random chance
    def visit_random_attraction(self):
        all_attractions = set(range(0, self.ATTRACTION_COUNT))
        possible_attractions = all_attractions - set(self.visited_attractions)
        return random.randint(0, len(possible_attractions) - 1)

    # Calculate probabilities of visiting adjacent unvisited attractions
    def visit_probabilistic_attraction(self, pheromone_trails):
        current_attraction = self.visited_attractions[-1]
        all_attractions = set(range(0, self.ATTRACTION_COUNT))
        possible_attractions = all_attractions - set(self.visited_attractions)
        possible_indexes = []
        possible_probabilities = []
        total_probabilities = 0
        for attraction in possible_attractions:
            possible_indexes.append(attraction)
            pheromones_on_path = math.pow(pheromone_trails[current_attraction][attraction], self.ALPHA)
            heuristic_for_path = math.pow(1 / self.attraction_distances[current_attraction][attraction], self.BETA)
            probability = pheromones_on_path * heuristic_for_path
            possible_probabilities.append(probability)
            total_probabilities += probability
        possible_probabilities = [probability / total_probabilities for probability in possible_probabilities]
        return [possible_indexes, possible_probabilities, len(possible_attractions)]

    # Select an attraction using the probabilities of visiting adjacent unvisited attractions
    @staticmethod
    def roulette_wheel_selection(probabilities):
        slices = []
        total = 0
        possible_indexes = probabilities[0]
        possible_probabilities = probabilities[1]
        possible_attractions_count = probabilities[2]
        for i in range(0, possible_attractions_count):
            slices.append([possible_indexes[i], total, total + possible_probabilities[i]])
            total += possible_probabilities[i]
        spin = random.random()
        result = [s[0] for s in slices if s[1] < spin <= s[2]]
        return result[0]

    # Get the total distance travelled by this ant
    def get_distance_travelled(self):
        total_distance = 0
        for a in range(1, len(self.visited_attractions)):
            total_distance += self.attraction_distances[self.visited_attractions[a]][self.visited_attractions[a-1]]
        total_distance += self.attraction_distances[self.visited_attractions[0]][self.visited_attractions[len(self.visited_attractions) - 1]]
        return total_distance

    def print_info(self):
        print('Ant ', self.__hash__())
        print('Total attractions: ', len(self.visited_attractions))
        print('Total distance: ', self.get_distance_travelled())



# Set the number of attractions in the data set
# Best total distance for 5 attractions: 19
# Best total distance for 48 attractions: 33523

ATTRACTION_COUNT = 5
# Set the probability of ants choosing a random attraction to visit (0.0 - 1.0)
RANDOM_ATTRACTION_FACTOR = 0.0
# Set the weight for pheromones on path for selection
ALPHA = 4
# Set the weight for heuristic of path for selection
BETA = 7


# Configure parameters of problem
def config_parameters_problem(num_atractions, alpha, beta, random_attraction_factor):
    Ant.attraction_distances = []
    Ant.ATTRACTION_COUNT = num_atractions
    Ant.BETA = beta
    Ant.ALPHA = alpha
    Ant.RANDOM_ATTRACTION_FACTOR = random_attraction_factor
    # Initialize the 2D matrix for storing distances between attractions
    with open('attractions-' + str(num_atractions) + '.csv') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            Ant.attraction_distances.append(row)

attraction_distances = config_parameters_problem(ATTRACTION_COUNT, ALPHA, BETA, RANDOM_ATTRACTION_FACTOR)

