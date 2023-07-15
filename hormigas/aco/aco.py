from ant import Ant
import math 

class ACO:

    def __init__(self, number_of_ants_factor):
        self.number_of_ants_factor = number_of_ants_factor
        # Initialize the array for storing ants
        self.ant_colony = []
        # Initialize the 2D matrix for pheromone trails
        self.pheromone_trails = []
        # Initialize the best distance in swarm
        self.best_distance = math.inf
        self.best_ant = None

    # Initialize ants at random starting locations
    def setup_ants(self, number_of_ants_factor):
        number_of_ants = round(Ant.ATTRACTION_COUNT * number_of_ants_factor)
        self.ant_colony.clear()
        for i in range(0, number_of_ants):
            self.ant_colony.append(Ant())

    # Initialize pheromone trails between attractions
    def setup_pheromones(self):
        for r in range(0, len(attraction_distances)):
            pheromone_list = []
            for i in range(0, len(attraction_distances)):
                pheromone_list.append(1)
            self.pheromone_trails.append(pheromone_list)

    # Move all ants to a new attraction
    def move_ants(self, ant_population):
        for ant in ant_population:
            ant.visit_attraction(self.pheromone_trails)

    # Determine the best ant in the colony - after one tour of all attractions
    def get_best(self, ant_population):
        for ant in ant_population:
            distance_travelled = ant.get_distance_travelled()
            if distance_travelled < self.best_distance:
                self.best_distance = distance_travelled
                self.best_ant = ant
        return self.best_ant

    # Update pheromone trails based ant movements - after one tour of all attractions
    def update_pheromones(self, evaporation_rate):
        for x in range(0, ATTRACTION_COUNT):
            for y in range(0, ATTRACTION_COUNT):
                self.pheromone_trails[x][y] = self.pheromone_trails[x][y] * evaporation_rate
                for ant in self.ant_colony:
                    self.pheromone_trails[x][y] += 1 / ant.get_distance_travelled()

    # Tie everything together - this is the main loop
    def solve(self, total_iterations, evaporation_rate):
        self.setup_pheromones()
        for i in range(0, TOTAL_ITERATIONS):
            self.setup_ants(NUMBER_OF_ANTS_FACTOR)
            for r in range(0, ATTRACTION_COUNT - 1):
                self.move_ants(self.ant_colony)
            self.update_pheromones(evaporation_rate)
            self.best_ant = self.get_best(self.ant_colony)
            print(i, ' Best distance: ', self.best_ant.get_distance_travelled())


# Set the percentage of ants based on the total number of attractions
NUMBER_OF_ANTS_FACTOR = 0.5
# Set the number of tours ants must complete
TOTAL_ITERATIONS = 10000
# Set the rate of pheromone evaporation (0.0 - 1.0)
EVAPORATION_RATE = 0.4
aco = ACO(NUMBER_OF_ANTS_FACTOR)
aco.solve(TOTAL_ITERATIONS, EVAPORATION_RATE)