class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  # Vicini e costi: {nodo: costo}
        self.routing_table = {}  # {destinazione: (distanza, next_hop)}
    
    def initialize_table(self):
        # Inizializza la tabella di routing
        for neighbor, cost in self.neighbors.items():
            self.routing_table[neighbor] = (cost, neighbor)
        self.routing_table[self.name] = (0, self.name)  # Nodo a se stesso
    
    def update_table(self, neighbor, neighbor_table):
        updated = False
        for destination, (neighbor_dist, neighbor_next_hop) in neighbor_table.items():
            current_dist = self.routing_table.get(destination, (float('inf'), None))[0]
            new_dist = self.neighbors[neighbor] + neighbor_dist
            if new_dist < current_dist:
                self.routing_table[destination] = (new_dist, neighbor)
                updated = True
        return updated
    
    def __str__(self):
        table = "\n".join([f"{dest}: (dist={dist}, next_hop={hop})"
                           for dest, (dist, hop) in self.routing_table.items()])
        return f"Routing Table for {self.name}:\n{table}"


class Network:
    def __init__(self):
        self.nodes = {}
    
    def add_node(self, name):
        self.nodes[name] = Node(name)
    
    def add_link(self, node1, node2, cost):
        self.nodes[node1].neighbors[node2] = cost
        self.nodes[node2].neighbors[node1] = cost
    
    def initialize_tables(self):
        for node in self.nodes.values():
            node.initialize_table()
    
    def simulate_routing(self):
        converged = False
        iteration = 0
        while not converged:
            converged = True
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            for node in self.nodes.values():
                for neighbor in node.neighbors:
                    updated = node.update_table(neighbor, self.nodes[neighbor].routing_table)
                    if updated:
                        converged = False
            for node in self.nodes.values():
                print(node)


# Definizione della rete
network = Network()
network.add_node("A")
network.add_node("B")
network.add_node("C")
network.add_node("D")
network.add_node("E")

network.add_link("A", "B", 1)
network.add_link("B", "C", 2)
network.add_link("A", "C", 4)
network.add_link("C", "D", 1)
network.add_link("E", "D", 4)

# Inizializza e simula
network.initialize_tables()
network.simulate_routing()
