import random
import pygame
import time

class State:
    '''
        A class representing the state of a cell in the Mars exploration grid.
        Each cell can be in one of three states: empty, containing a hole, or containing goods.
        States are mutually exclusive - a cell can only be in one state at a time.

        Attributes:
            hole (bool): True if cell contains a hole, False otherwise
            goods (bool): True if cell contains goods, False otherwise
            empty (bool): True if cell is empty, False otherwise

        Methods:
            set_hole(): Sets the cell state to contain a hole
            set_good(): Sets the cell state to contain goods 
            set_empty(): Sets the cell state to empty
            isEmpty(): Checks if cell is empty
            isHole(): Checks if cell contains a hole
            isGood(): Checks if cell contains goods
    '''
    def __init__(self):
        self.set_empty()
    
    def set_hole(self):
        self._set_state(hole=True)

    def set_good(self):
        self._set_state(goods=True)

    def set_empty(self):
        self._set_state()

    def _set_state(self, hole=False, goods=False):
        self.hole = hole and not goods # H % ~ G
        self.goods = goods and not hole # ~H % G
        self.empty = not (self.hole or self.goods) # ~(H or G)
    
    # Predicate symboles
    def isEmpty(self):
        return (self.empty and not (self.hole or self.goods))
    def isHole(self):
        return (self.hole and not (self.empty or self.goods))
    def isGood(self):
        return (self.goods and not (self.empty or self.hole))

    def __str__(self):
        if self.hole:
            return "hole"
        elif self.goods:
            return "good"
        else :
            return "empty"

class Environment():
    def __init__(self):
        pass
    # observing environment (Partially or fully )
    def get_adjacent_blocks(self):
        pass
    # taking an action 
    def take_action(self):
        pass
    # updating the environment 
    def update_env(self):
        pass
    

class Mars_Exploration_ENV(Environment):
    """
    A class representing the Mars Exploration Environment.
    This environment simulates a grid-based Mars exploration scenario where an agent
    navigates through a field containing holes (hazards) and good items (resources).
    Attributes:
        num_hol (int): Number of holes/hazards in the environment
        num_good (int): Number of good items/resources in the environment
        grid (list): 2D grid representing the environment, containing State objects
        player_pos (tuple): Current position of the player as (y, x) coordinates
    Methods:
        init_grid(): Initializes the grid by randomly placing player, holes and good items
        get_adjacent_blocks(): Returns dictionary of adjacent blocks and their states
        update_env(): Updates the environment state (placeholder)
        take_action(): Executes an action in the environment (placeholder)
    Parameters:
        grid_h (int): Height of the grid. Defaults to 20
        grid_w (int): Width of the grid. Defaults to 20
        num_hol (int): Number of holes to randomly place in the grid. Defaults to 10
        num_good (int): Number of good items to randomly place in the grid. Defaults to 10
        init_random (bool): Weather to initialize the starting position of the player randomly
    """

    def __init__(self, grid_h=20,  grid_w=20, num_hol=10, num_good=10, init_random=False):
        super().__init__()
        self.num_hol = num_hol
        self.num_good = num_good 
        self.init_random = init_random

        self.is_lost = False
        self.is_finished = False

        self.grid = [[State() for _ in range(grid_w)] for _ in range(grid_h)]
        self.player_pos = None
        self.init_grid()
        self.update_env()
    
    def init_grid(self):
        """
        Initialize the game grid by randomly placing the player, holes, and goods.

        The function performs the following steps:
        1. Randomly places the player on an empty cell
        2. Randomly places holes on empty cells (avoiding player position)
        3. Randomly places goods on empty cells (avoiding player position and holes)

        Attributes modified:
            player_pos (tuple): The (x,y) coordinates of player's position
            grid (list): 2D grid where each cell's state is updated with holes and goods

        The number of holes and goods placed is determined by class attributes:
            num_hol (int): Number of holes to place
            num_good (int): Number of goods to place

        Returns:
            None
        """
        # initialize playyer position 
        if not self.init_random : 
            self.player_pos = (0, 0)
        else :
            self.player_pos = (random.randint(0, len(self.grid) - 1), random.randint(0, len(self.grid[0]) - 1))
        # initialize hols 
        holes_placed = 0
        while holes_placed < self.num_hol:
            x = random.randint(0, len(self.grid) - 1)
            y = random.randint(0, len(self.grid[0]) - 1)
            if (x, y) != self.player_pos and self.grid[x][y].empty:
                self.grid[x][y].set_hole()
                holes_placed += 1
        # initialize goods  
        goods_placed = 0
        while goods_placed < self.num_good:
            x = random.randint(0, len(self.grid) - 1)
            y = random.randint(0, len(self.grid[0]) - 1)
            if (x, y) != self.player_pos and self.grid[x][y].empty:
                self.grid[x][y].set_good()
                goods_placed += 1

    
    def get_adjacent_blocks(self):
        """
        Gets the adjacent blocks (up, down, left, right) of a given position in the grid.

        Returns:
            dict: A dictionary where keys are direction tuples (dy,dx) and values are the block types at those adjacent positions.
                  Only includes valid adjacent positions that are within grid boundaries.
                  Direction tuples are:
                  - (0,1): right
                  - (0,-1): left  
                  - (1,0): up
                  - (-1,0): down

        Example:
            >>> grid = [[1,2,3],[4,5,6],[7,8,9]]
            >>> get_adjacent_blocks((1,1))
            {(0,1): 6, (0,-1): 4, (1,0): 8, (-1,0): 2}
        """
        y, x = self.player_pos
        adjacents = {}
        directions = [(0,1), (0, -1), (1, 0), (-1,0)]
        for d_y, d_x in directions:
            y_p = y + d_y
            x_p = x + d_x
            if 0 <= y_p < len(self.grid) and 0 <= x_p< len(self.grid[0]):
                adjacents[(d_y, d_x)] = self.grid[y_p][x_p]
        return adjacents



    def take_action(self, action : tuple): # action must be the selected direction along adjacent 
        """
        Updates the game state based on the player's action and current position.
        Args:
            action (tuple): Direction vector (dy,dx) indicating the move to make
        Returns:
            tuple: New (y,x) position after taking the action
        Notes:
            - If player moves to a hole: game is lost
            - If player moves to a position with goods: collects goods and game is lost 
            - If player moves to an empty position: moves there and game is lost
            - Updates environment state after each move
        """
        y, x = self.player_pos
        d_y ,d_x = action
        y_p = y + d_y
        x_p = x + d_x

        # if the selected position has hole in it then move and decide player lost 
        if (self.grid[y_p][x_p].isHole()):
            self.is_lost = True
            self.is_finished = True
            self.update_env() 
            return False
        # if the selected position is reachable (No hole in it) and goods in it then move to it 
        elif ((not self.grid[y_p][x_p].isHole()) and self.grid[y_p][x_p].isGood()): # Rewrote the first condition for better comprehension
            self.grid[y_p][x_p].set_empty()
            
            self.player_pos = (y_p, x_p)
            self.update_env()
            return True
        # if the selected position is reachable move to it 
        elif ((not self.grid[y_p][x_p].isHole()) and self.grid[y_p][x_p].isEmpty()): # Rewrote the first condition for better comprehension
            self.grid[y_p][x_p]
            self.player_pos = (y_p, x_p)
            self.update_env()
            return True
        return False
        

    def update_env(self, screen_size=(800, 800)):
        """
        Updates and renders the game environment using Pygame.
        This method handles the visual representation of the game state, including the grid,
        player position, holes, and collectable goods. It initializes Pygame if necessary and
        draws all game elements on the screen.
        Parameters:
            screen_size (tuple): A tuple of (width, height) for the game window size.
                                Defaults to (800, 800).
        Returns:
            None
        Details:
            - Initializes Pygame and creates a window if not already done
            - Calculates cell dimensions based on grid and screen size
            - Fills background with Mars-like brown color
            - Draws the grid lines
            - Renders game elements:
                - Player: Green circle
                - Holes: Red circles
                - Goods: Blue circles
            - Updates the display
        Note:
            Requires Pygame to be installed and the following class attributes to be defined:
            - self.grid: 2D list representing the game grid
            - self.player_pos: Tuple (y, x) representing player position
        """
        self.check_for_goods()
        # Initialize Pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
            self.screen = pygame.display.set_mode(screen_size)
            pygame.display.set_caption("Mars Exploration")

        # Calculate cell size based on grid and screen dimensions
        cell_width = screen_size[0] // len(self.grid[0])
        cell_height = screen_size[1] // len(self.grid)

        # Fill background with Mars-like terrain color
        self.screen.fill((194, 138, 107))  # Lighter Mars surface color

        # Draw grid with enhanced visibility
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                pygame.draw.rect(self.screen, (160, 110, 90), rect, 2)  # Thicker grid lines

                center_x = x * cell_width + cell_width//2
                center_y = y * cell_height + cell_height//2
                radius = min(cell_width, cell_height)//3

                # Draw cell contents with improved visuals
                if (y, x) == self.player_pos:
                    # Player: Robot-like appearance
                    pygame.draw.circle(self.screen, (50, 205, 50), (center_x, center_y), radius)  # Main body
                    pygame.draw.circle(self.screen, (0, 100, 0), (center_x, center_y), radius, 3)  # Outline
                    
                elif self.grid[y][x].isHole():
                    # Hole: Crater-like appearance
                    pygame.draw.circle(self.screen, (139, 69, 19), (center_x, center_y), radius)  # Dark crater
                    pygame.draw.circle(self.screen, (100, 30, 0), (center_x, center_y), radius, 3)  # Rim
                    
                elif self.grid[y][x].isGood():
                    # Good items: Crystal-like appearance
                    points = [
                        (center_x, center_y - radius),  # Top
                        (center_x + radius, center_y),  # Right
                        (center_x, center_y + radius),  # Bottom
                        (center_x - radius, center_y)   # Left
                    ]
                    pygame.draw.polygon(self.screen, (100, 149, 237), points)  # Crystal shape
                    pygame.draw.polygon(self.screen, (0, 0, 139), points, 2)   # Outline

        pygame.display.flip()

    def check_for_goods(self):
        """
        Checks if there are any goods remaining in the grid.
        Returns:
            bool: True if at least one good exists, False otherwise
        """
        for row in self.grid:
            for cell in row:
                if cell.isGood():
                    return True
                
        self.is_finished = True
        return False
    