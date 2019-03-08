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


class Traverser:
    def __init__(self, new_player):
        self.player = new_player
        self.grid = {}
        self.x = 0
        self.y = 0
        self.final_path = []
        self.path = []
        self.bread_crumbs = []

    def get_room_info(self, x, y):
        #
        id_room = F'({x}, {y})'
        #
        grid_value_current = 0
        if id_room in self.grid:
            grid_value_current = self.grid[id_room]
        return grid_value_current

    def set_room_info(self, x, y, info):
        #
        id_room = F'({x}, {y})'
        self.grid[id_room] = info

    def get_direction(self, direction):
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
        #
        grid_value = self.get_room_info(self.x, self.y)
        grid_value |= EXPLORED
        self.final_path = self.path
        #
        if room.n_to:
            grid_value |= NORTH
        if room.s_to:
            grid_value |= SOUTH
        if room.e_to:
            grid_value |= EAST
        if room.w_to:
            grid_value |= WEST
        #
        self.set_room_info(self.x, self.y, grid_value)

    def move(self, direction):
        #
        direction_char = DIRECTION_CHARS[direction]
        self.path.append(direction_char)
        #
        self.player.travel(direction_char)
        current_room = self.player.currentRoom
        #
        self.x = current_room.x
        self.y = current_room.y

    def direction_toward(self, x, y):
        if y > self.y:
            return NORTH
        if y < self.y:
            return SOUTH
        if x > self.x:
            return EAST
        if x < self.x:
            return WEST

    def traverse(self):
        while(True):  # Loop because Python throws an error with recursion
            #
            current_room = self.player.currentRoom
            self.x = current_room.x
            self.y = current_room.y
            current_room_info = self.get_room_info(self.x, self.y)
            if not (current_room_info & EXPLORED):
                self.explore_room(self.player.currentRoom)
            current_room_info = self.get_room_info(self.x, self.y)
            #
            next_direction = 0
            for direction in [NORTH, SOUTH, EAST, WEST]:
                if not (current_room_info & direction):
                    continue
                if self.get_direction(direction) & EXPLORED:
                    continue
                next_direction = direction
            #
            if next_direction:
                crumb = (self.x, self.y)
                self.bread_crumbs.append(crumb)
                self.move(next_direction)
                continue
            #
            elif len(self.bread_crumbs):
                crumb = self.bread_crumbs.pop()
                crumb_direction = self.direction_toward(crumb[0], crumb[1])
                if not crumb_direction:
                    raise Exception(F"no direction: ({self.x}, {self.y}) to ({crumb[0]}, {crumb[1]})")
                self.move(crumb_direction)
                continue
            #
            break
        #
        return self.final_path
