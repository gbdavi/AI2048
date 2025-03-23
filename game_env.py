import gym
from gym import spaces
import numpy as np
from game import Game2048  # Assuming your Game2048 class is in Game2048.py

class Game2048Env(gym.Env):
    def __init__(self):
        super(Game2048Env, self).__init__()
        self.game = Game2048(size=4)  # Initialize your custom 2048 game
        self.grid_size = self.game.size

        # Define observation space: 4x4 grid with possible values up to 2048
        self.observation_space = spaces.Box(low=0, high=2048, shape=(self.grid_size, self.grid_size), dtype=np.int32)

        # Define action space: 4 possible moves (up, down, left, right)
        # 0: up, 1: down, 2: left, 3: right
        self.action_space = spaces.Discrete(4)

    def _log2_transform(self, grid):
        """Apply log2 transformation while handling zeros safely."""
        transformed = np.log2(np.where(grid > 0, grid, 1))
        return transformed

    def reset(self):
        # Reset the game and return the initial state
        self.game = Game2048(size=4)
        return self.game.grid

    def step(self, action):
        # Map actions to the respective moves
        action_mapping = {
            0: 'up',
            1: 'down',
            2: 'left',
            3: 'right'
        }
        move = action_mapping.get(action, 'left')
        prev_score = self.game.score

        # Make the move
        if self.game.move(move):
            new_score = self.game.score

            # Calculate reward: difference in score
            reward = new_score - prev_score
        else:
            reward = -50

        # Check if the game is over
        done = self.game.game_over

        # Get transformed state
        new_state = self._log2_transform(self.game.grid)
        
        # No additional information needed
        info = {}

        # Return new state, reward, done flag, and info
        return new_state, reward, done, info

    def render(self, mode='human'):
        # Display the game grid and score
        self.game.render()
