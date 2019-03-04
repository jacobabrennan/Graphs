

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

    def traverse_breath_first(self, start_id):
        """"""
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
