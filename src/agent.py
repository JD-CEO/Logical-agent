from environments import Mars_Exploration_ENV
import time
import random
import sys




def call_method_on_objects(obj_list, method_name):
    results = []
    for obj in obj_list:
        method = getattr(obj, method_name)
        result = method() 
        results.append(result) 
    return results


class FOL_Agent():
    def __init__(self, environment):
        self.env = environment
        self.current_state = None
        self.adjacent_states = None
        # self.actions = [(0,1), (0, -1), (1, 0), (-1,0)]


    def _disjuntion(self, b_list):
        binary_list = [1 if x else 0 for x in b_list]
        return bool(max(binary_list))

    def _conjuntion(self, b_list):
        binary_list = [1 if x else 0 for x in b_list]
        return bool(min(binary_list))


    def filter_adjacency(self, adj_dict, direction):
        """
        Removes a specified direction from an adjacency dictionary and returns remaining values as a list
        
        Args:
            adj_dict (dict): Dictionary of adjacent positions and their states
            direction (tuple): Direction tuple (dy,dx) to remove
            
        Returns:
            list: List of remaining State objects after removing specified direction
        """
        filtered_dict = adj_dict.copy()
        filtered_dict.pop(direction, None)
        return list(filtered_dict.values())
    

    """
    DFS for Agent Navigation:

    This function enables an agent to explore a grid-based environment
    using DFS while avoiding obstacles and adhering to movement rules.

        Marks the current position as visited.
        Retrieves adjacent blocks and determines valid movement directions.
        Moves to each valid adjacent block and continues the DFS search.
        Implements backtracking when no further movement is possible.
        Terminates execution when the goal is reached.
    """

    def dfs(self, cur, adj_blks):
        cur.set_seen()
        adj = agent.env.get_adjacent_blocks()
        opt = []
        for itm in adj_blks.items():
                direction, block = itm
                # if the block is 
                r_neig = self.filter_adjacency(adj_blks, direction) # list of remaining neighbors
                selected = (block.isGood()) or ((not block.isHole()) and ( not self._disjuntion(call_method_on_objects(r_neig, "isGood")))) # defined rule
                
                if selected and not block.isSeen():
                    opt.append(itm)

        for itm in opt:
            direc, nxt = itm
            print("dir: ",direc)
            id_act, is_finished = agent.env.take_action(direc)
            time.sleep(0.1)
            if is_finished :
                sys.exit()
            self.dfs(nxt, agent.env.get_adjacent_blocks())
            back_dir = (0, 0)
            if direc == (1, 0):
                back_dir = (-1, 0)
            if direc == (0, 1):
                back_dir = (0, -1)    
            if direc == (-1, 0):
                back_dir = (1, 0)
            if direc == (0, -1):
                back_dir = (0, 1)
            print("back: ",back_dir)
            id_act, is_finished = agent.env.take_action(back_dir) 
            time.sleep(0.1)
            if is_finished :
                sys.exit()

        return 


if __name__ == "__main__":
    env = Mars_Exploration_ENV(grid_h=15,grid_w=15, num_hol=20, num_good=20)
    agent = FOL_Agent(env)
    # print("!!!", agent.env.get_adjacent_blocks())
    # print("!!!", agent.env.get_current_position())
    agent.dfs(agent.env.get_current_position(), agent.env.get_adjacent_blocks())
    # for i in range(1000): 
        # Observe environment
        # adj_blks = agent.env.get_adjacent_blocks()
        # Select action
        # action = agent.action_selection(adj_blks)
        # take selected action
        # did_act, is_finished = agent.env.take_action(action)
        # if is_finished:
        #     break
        # time.sleep(0.1)
    print("The agent completly extracted all goods") 

