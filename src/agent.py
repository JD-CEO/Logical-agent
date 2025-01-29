from environments import Mars_Exploration_ENV
import time
import random

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


    def action_selection(self, adj_blks):
        # define the gamma array in FOL => gamma : Is a list of well defined formulas 
        
        # define if each block is provable via the gamma 
        available_actions = []
        for direction, block in adj_blks.items():
            # if the block is 
            r_neig = self.filter_adjacency(adj_blks, direction) # list of remaining neighbors
            selected = (block.isGood()) or ((not block.isHole()) and ( not self._disjuntion(call_method_on_objects(r_neig, "isGood")))) # defined rule
            
            if selected :
                available_actions.append(direction)

        if available_actions:
            return random.choice(available_actions)
        return None
    







if __name__ == "__main__":
    env = Mars_Exploration_ENV(grid_h=7,grid_w=7, num_hol=5, num_good=5)
    agent = FOL_Agent(env)
    for i in range(1000): 
        # Observe environment
        adj_blks = agent.env.get_adjacent_blocks()
        # Select action
        action = agent.action_selection(adj_blks)
        # take selected action
        did_act, is_finished = agent.env.take_action(action)
        if is_finished:
            break
        time.sleep(0.1)
    print("The agent completly extracted all goods") 

