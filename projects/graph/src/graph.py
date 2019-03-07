

"""Simple graph implementation"""

# - Dependencies ---------------------------------
from queue import Queue


class Graph:
    """
    Represent a graph as a dictionary of vertices mapping labels to edges.
    """
    def __init__(self):
        self.vertices = dict()

    def add_vertex(self, vertex_id):
        """Creates a new vertex with no edges."""
        self.vertices[vertex_id] = set()

    def add_edge(self, source_id, end_id):
        """Connects two vertices along an edge, bidirectionally."""
        # Ensure endpoints are valid vertices on the graph
        if not (source_id in self.vertices):
            raise Exception('Invalid vertex id for edge source.')
        if not (end_id in self.vertices):
            raise Exception('Invalid vertex id for edge destination.')
        # Connect vertices symmetrically
        vertex_source = self.vertices[source_id]
        vertex_source.add(end_id)
        vertex_end = self.vertices[end_id]
        vertex_end.add(source_id)

    def traverse_breadth_first(self, start_id):
        """Prints a path of vertices visited, starting at a given vertex."""
        path = []
        # Define the open and closed vertices trackers
        open_vertices = Queue()
        closed_vertices = set()
        # Iterate over each vertex
        open_vertices.put(start_id)
        while not open_vertices.empty():
            # Skip nodes already visited
            current_id = open_vertices.get()
            if current_id in closed_vertices:
                continue
            # Add each vertex to the path
            path.append(current_id)
            closed_vertices.add(current_id)
            # Queue-up linked vertices
            current_vertex = self.vertices[current_id]
            for linked_id in current_vertex:
                open_vertices.put(linked_id)
        # Print path
        print(F'Path: {path}')

    def traverse_depth_first_stack(self, start_id):
        """Prints a path of vertices visited, starting at a given vertex."""
        path = []
        # Define the open and closed vertices trackers
        open_vertices = []
        closed_vertices = set()
        # Iterate over each vertex
        open_vertices.append(start_id)
        while len(open_vertices):
            # Skip nodes already visited
            current_id = open_vertices.pop()
            if current_id in closed_vertices:
                continue
            # Add each vertex to the path
            path.append(current_id)
            closed_vertices.add(current_id)
            # Stack linked vertices
            current_vertex = self.vertices[current_id]
            for linked_id in current_vertex:
                open_vertices.append(linked_id)
        # Print path
        print(F'Path: {path}')

    def search_breadth_first(self, id_start, id_end):
        path = []
        # Define the open and closed vertices trackers
        vertices_open = Queue()
        vertices_closed = set()
        # Iterate over each vertex
        vertices_open.put(id_start)
        while not vertices_open.empty():
            # Skip nodes already visited
            id_current = vertices_open.get()
            if id_current in vertices_closed:
                continue
            # Add each vertex to the path
            path.append(id_current)
            vertices_closed.add(id_current)
            # Check if end vertex has been reached
            current_vertex = self.vertices[id_current]
            if id_end in current_vertex:
                path.append(id_end)
                break
            # Queue-up linked vertices
            for id_linked in current_vertex:
                vertices_open.put(id_linked)
    
    def bfs(self, starting_vertex_id, target_id):
        q = Queue()
        visited = set()
        q.enqueue([starting_vertex_id])
        while q.size() > 0:
            path = q.dequeue()
            v = path[-1]
            if v not in visited:
                visited.add(v)
                if v == target_id:
                    return path
                for neighbor in self.verticies[v]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    q.enqueue(new_path)

test_graph = Graph()
test_graph.add_vertex('A')
test_graph.add_vertex('B')
test_graph.add_vertex('C')
test_graph.add_vertex('D')
test_graph.add_vertex('E')
test_graph.add_vertex('F')
test_graph.add_vertex('G')
test_graph.add_edge('A', 'A')
test_graph.add_edge('A', 'B')
test_graph.add_edge('B', 'C')
test_graph.add_edge('B', 'D')
test_graph.add_edge('B', 'E')
test_graph.add_edge('C', 'E')
test_graph.add_edge('D', 'E')
test_graph.add_edge('D', 'G')
test_graph.add_edge('E', 'F')
test_graph.traverse_depth_first_stack('C')
