

# = Traverser =================================================================
"""
The traverser object handles the AI / algorithm for moving the player object
through the world (rooms in a grid). It does this by performing a depth-first-
search on the room grid, marking rooms as explored after moving into them, and
skipping rooms which have already been explored. Movement "up" the tree, so as
to explore parallel branches, is acheived by placing rooms visited onto a stack
(bread_crumbs) and popping the last item from the stack whenever we need to
backtrack.

To use the traverser, instantiate it passing a player object as the single
argument to its constructor. Then call the traverse method, which returns a
path which visits every room in the world.

Instead of dealing with objects with numerous properties, each room is
represented as a single integer at a position in the grid. Each integer tracks
several bitflags representing exit directions and the explored status. Methods
are provided to get and set these flags both by grid coordinates and direction
from the traverser's current position.
"""


# - Project Constants ----------------------------
NORTH = 1
SOUTH = 2
EAST = 4
WEST = 8
EXPLORED = 16
DIRECTION_CHARS = {
    NORTH: 'n',
    SOUTH: 's',
    EAST: 'e',
    WEST: 'w',
}


# - Traverser Implementation ---------------------
class Traverser:
    """Manages the traversal of a player through the grid via self.traverse."""
    def __init__(self, new_player):
        self.player = new_player
        self.grid = {}
        self.x = 0
        self.y = 0
        self.final_path = []
        self.path = []
        self.bread_crumbs = []
    
    def traverse(self):
        """Calculates a path that traverses the entire grid."""
        self.x = self.player.currentRoom.x
        self.y = self.player.currentRoom.y
        while(True):  # Loop because Python throws an error with recursion
            # Get exits and explored status of current room
            current_room_info = self.get_room_info(self.x, self.y)
            # Explore current location, if necessary
            if not (current_room_info & EXPLORED):
                self.explore_room(self.player.currentRoom)
                current_room_info = self.get_room_info(self.x, self.y)
            # Check for directions in need of exploration
            next_direction = 0
            for direction in [NORTH, SOUTH, EAST, WEST]:
                if not (current_room_info & direction):
                    continue
                if self.get_direction(direction) & EXPLORED:
                    continue
                next_direction = direction
            # Explore, if possible
            if next_direction:
                crumb = (self.x, self.y)
                self.bread_crumbs.append(crumb)
                self.move(next_direction)
                continue
            # If exploration is exhausted backtrack (if possible)
            elif len(self.bread_crumbs):
                crumb = self.bread_crumbs.pop()
                crumb_direction = self.direction_toward(crumb[0], crumb[1])
                if not crumb_direction:
                    raise Exception(F"no direction: ({self.x}, {self.y}) to ({crumb[0]}, {crumb[1]})")
                self.move(crumb_direction)
                continue
            # Stop once neither backtracking nor exploration are possible
            break
        # Return the path from the last exploration
        # (that is, don't include the backtrack to the start room)
        return self.final_path

    def get_room_info(self, x, y):
        """Returns the exits and explored status of the room at (x,y)."""
        # Uniquely identify this grid location
        id_room = F'({x}, {y})'
        # Find and return the value associated with that grid location
        grid_value_current = 0
        if id_room in self.grid:
            grid_value_current = self.grid[id_room]
        return grid_value_current

    def set_room_info(self, x, y, info):
        """Sets the exits and explored status of the room at (x,y)."""
        id_room = F'({x}, {y})'
        self.grid[id_room] = info

    def get_direction(self, direction):
        """
        Gets the exits and explored status in the direction from current (x,y).
        """
        new_x = self.x
        new_y = self.y
        if direction & NORTH:
            new_y += 1
        if direction & SOUTH:
            new_y -= 1
        if direction & EAST:
            new_x += 1
        if direction & WEST:
            new_x -= 1
        return self.get_room_info(new_x, new_y)

    def explore_room(self, room):
        """Sets explored status and calculates the exit flags."""
        # Turn on explored bit, update path
        grid_value = self.get_room_info(self.x, self.y)
        grid_value |= EXPLORED
        self.final_path = self.path
        # Set exit bits
        if room.n_to:
            grid_value |= NORTH
        if room.s_to:
            grid_value |= SOUTH
        if room.e_to:
            grid_value |= EAST
        if room.w_to:
            grid_value |= WEST
        # Store flags in grid
        self.set_room_info(self.x, self.y, grid_value)

    def move(self, direction):
        """Moves the traverser to a new grid location."""
        # Update path
        direction_char = DIRECTION_CHARS[direction]
        self.path.append(direction_char)
        # Move the player object
        self.player.travel(direction_char)
        # Update current (x,y)
        current_room = self.player.currentRoom
        self.x = current_room.x
        self.y = current_room.y

    def direction_toward(self, x, y):
        """Returns the direction of travel from current loc to (x,y)."""
        if y > self.y:
            return NORTH
        if y < self.y:
            return SOUTH
        if x > self.x:
            return EAST
        if x < self.x:
            return WEST
