import csv
from math import sqrt
from collections import deque
from queue import PriorityQueue
import time

def read_coordinates():
    coordinates = {}
    with open("coordinates.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            coordinates[row[0]] = (float(row[1]), float(row[2]))
    return coordinates

def read_adjacencies():
    adjecencies = []
    with open("Adjacencies.txt", "r") as file:
        for line in file.readlines(): 
            pair = line.split()
            adjecencies.append([pair[0], pair[1]])   
            adjecencies.append([pair[1], pair[0]])      
    return adjecencies

def calculate_city_distance(city1, city2, coordinates):
    lat1, lon1 = coordinates[city1]
    lat2, lon2 = coordinates[city2]
    return sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def calculate_path_distance(path, coordinates):
    distance = 0.0
    for i in range(len(path) - 1):
        distance += calculate_city_distance(path[i], path[i + 1], coordinates)
    return distance

def get_cities():
    while True:
        city1 = input("Enter the origin city: ")
        if city1 not in coordinates.keys():
            print("City not valid. Please enter a valid city.")
        else:
            break
    while True:
        city2 = input("Enter the destination city: ")
        if city2 not in coordinates.keys():
            print("City not valid. Please enter a valid city.")
        else:
            break
    return city1, city2;

def bfs(adjecencies, coordinates, city1, city2):
    queue = deque([(city1, [city1])])
    visited = set()
    while queue:
        current, path = queue.popleft()
        if current == city2:
            return path
        if current in visited:
            continue
        visited.add(current)
        for i in [pair[1] for pair in adjecencies if pair[0] == current]:
            if i not in visited:
                queue.append((i, path + [i]))
    return None

def dfs(adjecencies, coordinates, city1, city2):
    stack = [(city1, [city1])]
    visited = set()
    while stack:
        current, path = stack.pop()
        if current == city2:
            return path
        if current in visited:
            continue
        visited.add(current)
        for i in [pair[1] for pair in adjecencies if pair[0] == current]:
            if i not in visited:
                stack.append((i, path + [i]))    
    return None

def id_dfs(adjecencies, coordinates, city1, city2, depth=46):
    # depth limited search first
    def dls(node, path, depth):
        if node == city2:
            return path
        if depth <= 0:
            return None
        for i in [pair[1] for pair in adjecencies if pair[0] == node]:
            if i not in path:
                result = dls(i, path + [i], depth - 1)
                if result:
                    return result
        return False
    
    for i in range(1, depth + 1):
        result = dls(city1, [city1], i)
        if result:
            return result
    return False

def best_first(adjacencies, coordinates, city1, city2):
    pq = PriorityQueue()
    pq.put((calculate_city_distance(city1, city2, coordinates), city1, [city1]))
    visited = set()
    while not pq.empty():
        _, current, path = pq.get()
        if current == city2:
            return path
        if current in visited:
            continue
        visited.add(current)
        for i in [pair[1] for pair in adjecencies if pair[0] == current]:
            pq.put((calculate_city_distance(i, city2, coordinates), i, path + [i]))
    return None

def a_star(adjecencies, coordinates, city1, city2):
    pq = PriorityQueue()
    pq.put((0, city1, [city1], 0))
    visited = set()
    while not pq.empty():
        _, current, path, cost = pq.get()
        if current == city2:
            return path
        if current in visited:
            continue
        visited.add(current)
        for i in [pair[1] for pair in adjecencies if pair[0] == current]:
            pq.put((cost + calculate_city_distance(i, city2, coordinates), i, path + [i], cost + calculate_city_distance(current, i, coordinates)))
    return None

def get_search_method():
    while True:
        search_method = input("Enter the search method (bfs, dfs, id-dfs, best_first, a_star): ")
        if search_method not in ["bfs", "dfs", "id-dfs", "best_first", "a_star"]:
            print("Search method not valid. Please enter a valid search method.")
        else:
            break
    return search_method

if __name__ == "__main__":
    coordinates = read_coordinates()
    adjecencies = read_adjacencies()
    while True:
        city1, city2 = get_cities()
        search_method = get_search_method()
        
        start_time = time.time()
        if search_method == "bfs":
            path = bfs(adjecencies, coordinates, city1, city2)
        elif search_method == "dfs":
            path = dfs(adjecencies, coordinates, city1, city2)
        elif search_method == "id-dfs":
            path = id_dfs(adjecencies, coordinates, city1, city2)
        elif search_method == "best_first":
            path = best_first(adjecencies, coordinates, city1, city2)
        elif search_method == "a_star":
            path = a_star(adjecencies, coordinates, city1, city2)
        end_time = time.time()

        distance = calculate_path_distance(path, coordinates)
        print("Path: ", path, "\n" )
        print(f"Path distance: {distance:.2f} km")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
        if input("Do you want to search for another path? (y/n): ") != "y":
            break
        

    
    
