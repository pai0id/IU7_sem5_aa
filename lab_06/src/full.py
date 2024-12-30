def calculate_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    total_distance += distance_matrix[route[-1]][route[0]]
    return total_distance

def find_routes(current_city, visited, route, distance_matrix, all_routes):
    if len(visited) == len(distance_matrix):
        all_routes.append(route[:])
        return

    for next_city in range(len(distance_matrix)):
        if next_city not in visited:
            visited.add(next_city)
            route.append(next_city)
            find_routes(next_city, visited, route, distance_matrix, all_routes)
            route.pop()
            visited.remove(next_city)

def full_search(distance_matrix):
    n = len(distance_matrix)
    all_routes = []
    visited = set()
    
    visited.add(0)
    find_routes(0, visited, [0], distance_matrix, all_routes)

    min_distance = float('inf')
    best_route = None

    for route in all_routes:
        current_distance = calculate_distance(route, distance_matrix)
        if current_distance < min_distance:
            min_distance = current_distance
            best_route = route

    return best_route, min_distance


if __name__ == "__main__":
    # distance_matrix = [
    #     [0, 10, 15, 20],
    #     [10, 0, 35, 25],
    #     [15, 35, 0, 30],
    #     [20, 25, 30, 0]
    # ]

    distance_matrix = [
        [0, 29, 20, 21, 16, 31, 100, 12, 4, 31],
        [29, 0, 15, 17, 28, 40, 72, 21, 29, 41],
        [20, 15, 0, 28, 12, 25, 81, 18, 24, 30],
        [21, 17, 28, 0, 23, 39, 63, 12, 18, 25],
        [16, 28, 12, 23, 0, 30, 75, 14, 21, 27],
        [31, 40, 25, 39, 30, 0, 50, 30, 35, 45],
        [100, 72, 81, 63, 75, 50, 0, 90, 100, 80],
        [12, 21, 18, 12, 14, 30, 90, 0, 10, 15],
        [4, 29, 24, 18, 21, 35, 100, 10, 0, 20],
        [31, 41, 30, 25, 27, 45, 80, 15, 20, 0]
    ]

    best_route, min_distance = full_search(distance_matrix)
    print("Лучший маршрут:", best_route)
    print("Минимальное расстояние:", min_distance)
