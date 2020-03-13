def EditDistance(sequence1, sequence2):
    if len(sequence1) < len(sequence2):
        return EditDistance(sequence2, sequence1)

    if len(sequence2) == 0:
        return len(sequence1)

    prev = range(len(sequence2) + 1)
    for i, c1 in enumerate(sequence1):
        curr = [i + 1]
        for j, c2 in enumerate(sequence2):
            inserts = prev[j + 1] + 1
            dels = curr[j] + 1
            subs = prev[j] + (c1 != c2)
            curr.append(min(inserts, dels, subs))
        prev = curr
    
    return prev[-1]

class PhylNode:
    def __init__(self, distance=None, sequence=None, children=[]):
        self.distance = distance
        self.sequence = sequence
        self.children = children if children else []
        
    def get_children(self):
        return self.children
        
    def add_child(self, node):
        self.children.append(node)
        
    def get_distance(self):
        return self.distance
        
    def set_distance(self, distance):
        self.distance = distance
        
    def get_sequence(self):
        return self.sequence
    
    def set_sequence(self, sequence):
        self.sequence = sequence

        
class PhylTree:
    def __init__(self, node):
        self.r = node
        
    def root(self):
        return self.r
        
    def distance_sum(self):
        d = 0
        nodes = [self.root()]
        while nodes:
            node = nodes.pop()
            d += node.get_distance()
            nodes += node.get_children()
        return d
        
    def get_sequences(self):
        sequences = []
        nodes = [self.root()]
        while nodes:
            node = nodes.pop()
            sequences.append(node.get_sequence())
            nodes = nodes + node.get_children()[::-1]
        return sequences
        
    def calculate_distances(self, dist_function=EditDistance):
        r = self.root()
        r.set_distance(0)
        nodes = [r]
        while nodes:
            node = nodes.pop()
            parent_sequence = node.get_sequence()
            for child in node.get_children():
                nodes.append(child)
                child.set_distance(dist_function(parent_sequence, child.get_sequence()))
    
    def BuildTree(self, sequences, dist_function=EditDistance):
        n = len(sequences)
        if n == 1:
            return PhylTree(PhylNode(0, sequences[0]))
        edges = []
        for i in range(n):
            sequence_i = sequences[i]
            for j in range(i+1,n):
                edges.append((dist_function(sequence_i, sequences[j]),i,j))
        edges.sort()
        
        connected = [False] * n
        tree_edges = []
        for (dist,v1,v2) in edges:
            if connected[v1] and connected[v2]:
                continue
            connected[v1] = True
            connected[v2] = True
            tree_edges.append((dist,v1,v2))
        
        not_connected = [True] * n
        nodes = [PhylNode(0,sequence) for sequence in sequences]
        dist,v,r = tree_edges.pop(0)
        not_connected[v] = not_connected[r] = False
        nodes[v].set_distance(dist)
        nodes[r].add_child(nodes[v])

        while tree_edges:
            dist,v1,v2 = tree_edges.pop(0)
            if not_connected[v1] and not_connected[v2]:
                tree_edges.append((dist,v1,v2))
                continue
            
            if not_connected[v2]: v1,v2 = v2,v1
            
            not_connected[v1] = False
            nodes[v1].set_distance(dist)
            nodes[v2].add_child(nodes[v1])

        return PhylTree(nodes[r])
