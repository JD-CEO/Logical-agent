from environments import Mars_Exploration_ENV, State


class FOL_Agent():
    def __init__(self, environment):
        self.env = environment
        self.current_state = None
        self.adjacent_states = None
        self.actions = [(0,1), (0, -1), (1, 0), (-1,0)]

    def action_selection(self):
        adj_blks = self.env.get_adjacent_blocks()
        print(adj_blks)
        # define the gamma array in FOL => gamma : Is a list of well defined formulas 

        # define if each block is provable via the gamma 








if __name__ == "__main__":
    env = Mars_Exploration_ENV()
    agent = FOL_Agent(env)
    for i in range(100): 
        agent.action_selection()
    