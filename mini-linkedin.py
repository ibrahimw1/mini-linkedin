import requests
import sys
from enum import Enum

# Sending a request to the container
res = requests.get("http://localhost:3338/graph").json()

# Getting the "adjacency map" field from the response
adjacency_map = res["adjacency_map"]

# Define an Enum for colors used in graph traversal
class Color(Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2

# Define a Vertex class to represent nodes in the graph
class Vertex:
    def __init__(self, name) -> None:
        self.name = name
        self.color = Color.WHITE  # Initialize color to WHITE
        self.d = 0               # Discovery time
        self.f = float("inf")    # Finish time
        self.parent = None        # Parent node in DFS tree
        self.neighbors = []       # Adjacent vertices

    def add_neighbors(self, neighbors):
        self.neighbors.extend(neighbors)

# Define a Graph class to represent the graph and perform graph operations
class Graph:
    def __init__(self) -> None:
        self.vertices = []      # List to store vertices
        self.time = 0            # Global time variable for DFS
        self.cyclic = False      # Flag to detect cycles in the graph
        self.stack = []          # Stack to store vertices in DFS order
        self.adj = {}            # Adjacency dictionary

    def add_vertices(self, vertices):
        self.vertices.extend(vertices)

    # Depth-First Search (DFS) helper function
    def dfs_visit(self, u: Vertex):
        self.time += 1
        u.d = self.time
        u.color = Color.GRAY
        print(u.name)  # Print the name of the visited vertex
        for v in u.neighbors:
            if v.color == Color.WHITE:
                v.parent = u
                self.dfs_visit(v)
            elif v.color == Color.GRAY:
                self.cyclic = True  # Detect a cycle if a gray vertex is encountered

        self.time += 1
        u.f = self.time
        u.color = Color.BLACK
        self.stack.append(u)

    # Add a vertex to the adjacency dictionary
    def add_vertex(self, key, neighbors=[]):
        self.adj[key] = neighbors

    # Breadth-First Search (BFS) function
    def bfs(self, source):
        if source not in self.adj:
            print(f"Vertex '{source}' not found in the graph.")
            return
        
        print(source)
        level = {source: 0}
        parent = {source: None}
        i = 1
        frontier = [source]
        while frontier:
            nxt = []
            for u in frontier:
                for v in self.adj[u]:
                    if v not in level:
                        print(v)
                        level[v] = i
                        parent[v] = u
                        nxt.append(v)
            frontier = nxt
            i += 1
        
        return level

    # Depth-First Search (DFS) function
    def dfs(self):
        for u in self.vertices:
            if u.color == Color.WHITE:
                self.dfs_visit(u)
        return self.stack
    
    # Display the network using DFS
    def show_network(self):
        dfs = self.dfs()
        num_visited = len(dfs)
        print("Number of Vertices visited: ", num_visited)
    
    # Show connections of a specific person using BFS
    def show_connections(self, person):
        levels = self.bfs(person)

        if levels is None:
            print(f"Person '{person}' not found in the network.")
            return

        first_connections = {name for name, lvl in levels.items() if lvl == 1}
        second_connections = {name for name, lvl in levels.items() if lvl == 2}
        third_connections = {name for name, lvl in levels.items() if lvl == 3}

        print("\nNetwork of:", person)
        print("1st Connections [", len(first_connections), "in total]: ", first_connections)
        print()
        print("2nd Connections [", len(second_connections), "in total]: ", second_connections)
        print()
        print("3rd Connections [", len(third_connections), "in total]: ", third_connections)
        print()

    # Connect two people in the network
    def connect(self, person_1, person_2):
        vertex_1 = None
        vertex_2 = None

        # Find the vertex objects corresponding to the person names
        for vertex in self.vertices:
            if vertex.name == person_1:
                vertex_1 = vertex
            elif vertex.name == person_2:
                vertex_2 = vertex

        if vertex_1 is None or vertex_2 is None:
            print("Not found in the network.")
            return

        # Update adjacency map by adding each person to the other's neighbors
        vertex_1.neighbors.append(vertex_2)
        vertex_2.neighbors.append(vertex_1)

        # Update the adj dictionary
        if person_1 in self.adj:
            self.adj[person_1].append(person_2)
        else:
            self.adj[person_1] = [person_2]

        if person_2 in self.adj:
            self.adj[person_2].append(person_1)
        else:
            self.adj[person_2] = [person_1]

        print(f"Connected {person_1} and {person_2}.")

# Instantiate the Graph class
graph = Graph()

# Create vertices
vertices = []
for vertex_name in adjacency_map.keys():
    vertex = Vertex(vertex_name)
    vertices.append(vertex)

# Add neighbors to the vertices
for vertex in vertices:
    neighbor_names = adjacency_map[vertex.name]
    neighbors = [v for v in vertices if v.name in neighbor_names]
    vertex.add_neighbors(neighbors)

# Update the graph's adjacency dictionary using the adjacency_map
for vertex_name, neighbors in adjacency_map.items():
    graph.add_vertex(vertex_name, neighbors)

# Add vertices to the graph
graph.add_vertices(vertices)

# Command-line argument handling
if sys.argv[1] == "show_network":
    graph.show_network()
elif sys.argv[1] == "show_connections":
    graph.show_connections(sys.argv[2])
elif sys.argv[1] == "connect":
    graph.connect(sys.argv[2], sys.argv[3])
    graph.show_connections(sys.argv[2])
else:
    print("Invalid command.")
