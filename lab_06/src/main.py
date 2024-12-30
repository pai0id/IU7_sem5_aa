from ant import *
from full import *
from csv_ import *
import numpy as np
import random
import pandas as pd

class GraphData:
    def __init__(self, graphs):
        """
        Класс данных для хранения нескольких графов
        :param graphs: Список матриц расстояний для различных графов
        """
        self.graphs = graphs

def evaluate_performance(ant_colony, true_distance, num_trials=10):
    deviations = []

    for _ in range(num_trials):
        _, best_distance = ant_colony.run()
        deviation = abs(best_distance - true_distance)
        deviations.append(deviation)

    return min(deviations), max(deviations), np.mean(deviations)

def parameterize(graphs, alpha_values, evaporation_values, num_iterations_values, true_distances, num_ants=10, num_trials=10):
    results = []

    for graph_idx, graph in enumerate(graphs):
        for alpha in alpha_values:
            for evaporation_rate in evaporation_values:
                for num_iterations in num_iterations_values:
                    ant_colony = AntColony(
                        distance_matrix=graph,
                        num_ants=num_ants,
                        num_iterations=num_iterations,
                        alpha=alpha,
                        beta=1.0,
                        evaporation_rate=evaporation_rate,
                        elite_factor=1.5,
                        num_elite_ants=3
                    )

                    min_deviation, max_deviation, mean_deviation = evaluate_performance(ant_colony, true_distances[graph_idx], num_trials)
                        
                    results.append({
                        "Graph": graph_idx,
                        "Alpha": alpha,
                        "Evaporation Rate": evaporation_rate,
                        "Iterations": num_iterations,
                        "Min Deviation": min_deviation,
                        "Max Deviation": max_deviation,
                        "Mean Deviation": mean_deviation
                    })
    
    df = pd.DataFrame(results)
    df.to_csv("res.csv", index=False)
    return df



graphs = [
    [
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
    ],
    [
        [0, 42, 9, 13, 16, 21, 26, 31, 36, 46], 
        [42, 0, 7, 15, 19, 23, 29, 34, 39, 49], 
        [9, 7, 0, 12, 17, 21, 27, 32, 37, 47],  
        [13, 15, 12, 0, 10, 16, 21, 26, 31, 41],
        [16, 19, 17, 10, 0, 13, 19, 23, 29, 36],
        [21, 23, 21, 16, 13, 0, 11, 16, 21, 31],
        [26, 29, 27, 21, 19, 11, 0, 13, 16, 26],
        [31, 34, 32, 26, 23, 16, 13, 0, 11, 21],
        [36, 39, 37, 31, 29, 21, 16, 11, 0, 16],
        [46, 49, 47, 41, 36, 31, 26, 21, 16, 0] 
    ],
    [
        [0, 45, 11, 14, 18, 22, 27, 32, 37, 48],
        [45, 0, 9, 16, 20, 24, 31, 36, 41, 52], 
        [11, 9, 0, 12, 17, 21, 26, 31, 36, 46], 
        [14, 16, 12, 0, 10, 15, 20, 25, 30, 40],
        [18, 20, 17, 10, 0, 13, 19, 23, 29, 36],
        [22, 24, 21, 15, 13, 0, 11, 16, 21, 31],
        [27, 31, 26, 20, 19, 11, 0, 13, 16, 26],
        [32, 36, 31, 25, 23, 16, 13, 0, 11, 21],
        [37, 41, 36, 30, 29, 21, 16, 11, 0, 16],
        [48, 52, 46, 40, 36, 31, 26, 21, 16, 0] 
    ]
]

true_distances = [full_search(graphs[0])[1], full_search(graphs[1])[1], full_search(graphs[2])[1]]

alpha_values = [.1, .3, .5, .7, .9]
evaporation_values = [.1, .3, .5, .7, .9]
num_iterations_values = [5, 10, 20, 50, 100]

graph_data = GraphData(graphs)
results = parameterize(graph_data.graphs, alpha_values, evaporation_values, num_iterations_values, true_distances)

print(results)