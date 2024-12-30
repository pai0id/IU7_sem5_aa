import numpy as np
import random
from full import *
import matplotlib.pyplot as plt

class AntColony:
    def __init__(self, distance_matrix, num_ants, num_iterations, alpha, beta, evaporation_rate, elite_factor, num_elite_ants):
        self.distance_matrix = distance_matrix
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.elite_factor = elite_factor
        self.num_elite_ants = num_elite_ants
        self.num_cities = len(distance_matrix)
        self.pheromone_matrix = np.ones((self.num_cities, self.num_cities))

    def run(self):
        best_route = None
        best_distance = float('inf')

        for _ in range(self.num_iterations):
            all_routes = []
            all_distances = []

            for _ in range(self.num_ants):
                route = self.construct_route()
                distance = self.calculate_distance(route)
                all_routes.append(route)
                all_distances.append(distance)

                if distance < best_distance:
                    best_distance = distance
                    best_route = route

            sorted_indices = np.argsort(all_distances)
            elite_routes = [all_routes[i] for i in sorted_indices[:self.num_elite_ants]]
            elite_distances = [all_distances[i] for i in sorted_indices[:self.num_elite_ants]]

            self.update_pheromones(all_routes, all_distances, elite_routes, elite_distances, best_route, best_distance)

        return best_route, best_distance

    def construct_route(self):
        route = []
        visited = set()
        current_city = random.randint(0, self.num_cities - 1)
        route.append(current_city)
        visited.add(current_city)

        for _ in range(self.num_cities - 1):
            next_city = self.select_next_city(current_city, visited)
            route.append(next_city)
            visited.add(next_city)
            current_city = next_city

        return route

    def select_next_city(self, current_city, visited):
        probabilities = []
        total_pheromone = 0.0

        for city in range(self.num_cities):
            if city not in visited:
                pheromone = self.pheromone_matrix[current_city][city] ** self.alpha
                distance = self.distance_matrix[current_city][city]
                probability = pheromone / (distance ** self.beta)
                probabilities.append(probability)
                total_pheromone += probability
            else:
                probabilities.append(0)

        probabilities = [p / total_pheromone for p in probabilities]
        return np.random.choice(range(self.num_cities), p=probabilities)

    def calculate_distance(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.distance_matrix[route[i]][route[i + 1]]
        total_distance += self.distance_matrix[route[-1]][route[0]]
        return total_distance

    def update_pheromones(self, all_routes, all_distances, elite_routes, elite_distances, best_route, best_distance):
        self.pheromone_matrix *= (1 - self.evaporation_rate)

        for route, distance in zip(all_routes, all_distances):
            pheromone_deposit = 1.0 / distance
            for i in range(len(route) - 1):
                self.pheromone_matrix[route[i]][route[i + 1]] += pheromone_deposit
            self.pheromone_matrix[route[-1]][route[0]] += pheromone_deposit

        for elite_route, elite_distance in zip(elite_routes, elite_distances):
            elite_pheromone_deposit = self.elite_factor / elite_distance
            for i in range(len(elite_route) - 1):
                self.pheromone_matrix[elite_route[i]][elite_route[i + 1]] += elite_pheromone_deposit
            self.pheromone_matrix[elite_route[-1]][elite_route[0]] += elite_pheromone_deposit



if __name__ == "__main__":
    # distance_matrix = [
    #     [0, 10, 15, 20],
    #     [10, 0, 35, 25],
    #     [15, 35, 0, 30],
    #     [20, 25, 30, 0]
    # ]

    distance_matrix = [
        [0, 40, 10, 12, 15, 20, 25, 30, 35, 45],
        [40, 0, 8, 14, 18, 22, 30, 35, 40, 50], 
        [10, 8, 0, 11, 16, 20, 25, 30, 35, 45], 
        [12, 14, 11, 0, 9, 15, 20, 25, 30, 40], 
        [15, 18, 16, 9, 0, 12, 18, 22, 28, 35], 
        [20, 22, 20, 15, 12, 0, 10, 15, 20, 30],
        [25, 30, 25, 20, 18, 10, 0, 12, 15, 25],
        [30, 35, 30, 25, 22, 15, 12, 0, 10, 20],
        [35, 40, 35, 30, 28, 20, 15, 10, 0, 15],
        [45, 50, 45, 40, 35, 30, 25, 20, 15, 0] 
    ]

    num_ants = 10
    num_iterations = 100
    alpha = 0.3
    beta = 0.3
    evaporation_rate = 0.3
    elite_factor = 1.0

    t_val = full_search(distance_matrix)[1]

    n_vals = list(range(1, 5, 1))
    res = []

    for num_elite_ants in n_vals:
        ant_colony = AntColony(distance_matrix, num_ants, num_iterations, alpha, beta, evaporation_rate, elite_factor, num_elite_ants)
        _, best_distance = ant_colony.run()
        res.append(abs(best_distance - t_val))

    plt.plot(n_vals, res, marker='o')
    plt.title('Зависимость расстояния от числа элитных муравьев')
    plt.xlabel('Число элитных муравьев')
    plt.ylabel('Абсолютная разница в расстоянии')
    plt.grid()
    plt.xticks(n_vals)
    plt.savefig('ant_colony_results.png', format='png', dpi=300)
    print(res)
