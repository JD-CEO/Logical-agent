# Mars Exploration Environment

A grid-based environment for autonomous agent exploration with first-order logic constraints. Designed for developing and testing logical agents that navigate hazardous terrain while collecting resources.

## Features

- 🪐 Grid-based Mars terrain simulation
- 🕳️ Hazardous holes with logical constraints
- 📦 Collectible resource packages (goods)
- 🧠 First-order logic state representations
- 🎮 Pygame visualization system
- 🔄 Partially observable environment dynamics

## Installation

1. **Requirements**:
   - Python 3.8+
   - Pygame 2.0+

2. **Install Pygame**:
   ```bash
   pip install pygame
   ```

## Usage

from mars_exploration import Mars_Exploration_ENV

#Initialize environment
```env = Mars_Exploration_ENV(grid_h=15, grid_w=15, num_hol=20, num_good=15)

#Example agent interaction loop
while not env.is_finished:
    # Get adjacent blocks (agent's perception)
    adjacent = env.get_adjacent_blocks()
    
    # Simple policy: Move right whenever possible
    if (0, 1) in adjacent:
        success, _ = env.take_action((0, 1))
    
    env.update_env()
```
# Environment Rules & Logic
## Core Axioms

- State Exclusivity (∀ cells):

    ```∀c ∈ Grid, (Hole(c) → ¬Good(c) ∧ ¬Empty(c)) ∧
            (Good(c) → ¬Hole(c) ∧ ¬Empty(c)) ∧
            (Empty(c) → ¬Hole(c) ∧ ¬Good(c))
    ```
- Movement Constraints:

    ```SafeMove(d) ≡ ∃c ∈ Adjacent(d), ¬Hole(c)
    CollectGood(d) ≡ ∃c ∈ Adjacent(d), Good(c)
    ```

- Termination Conditions:
    ```GameOver ≡ ∃c ∈ Grid, (AtAgent(c) ∧ Hole(c)) ∨
            (∀c ∈ Grid, ¬Good(c))
    ```

- First-Order Logic Implementation
```
#State validation in take_action()
if cell.isHole():
    # ∀a ∈ Actions, EnterHole(a) → Terminate
    self.is_lost = True

elif cell.isGood():
    # ∃g ∈ Goods, Collect(g) → UpdateState(g, Empty)
    cell.set_empty()
```