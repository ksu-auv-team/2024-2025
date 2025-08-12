from typing import Any, Dict, Optional, Tuple
from dataclasses import dataclass
from config_loader import load_config
import numpy as np
import requests
import gym

from gym.spaces import Discrete
from gym.utils import seeding
from gym import spaces

class ImitationEnvironment(gym.Env):
    """
        @brief Imitation Learning Environment for Type X

        @details This environment simulates the behavior of a Type X agent for the purpose of imitation learning.

    """
    @dataclass
    class Inputs:
        id: int
        step_index: int
        direction: str
        force: float
        s1: float
        s2: float
        s3: float
        arm: bool

    @dataclass
    class Outputs:
        id: int
        step_index: int
        direction: str
        force: float
        s1: float
        s2: float
        s3: float
        arm: bool

    @dataclass
    class Observation:
        id: int
        step_index: int
        direction: str
        force: float
        s1: float
        s2: float
        s3: float
        arm: bool
        X_accel: float
        Y_accel: float
        Z_accel: float
        Roll: float
        Pitch: float
        Yaw: float
        reward: float

    def __init__(self):
        super().__init__()
        self.config = load_config("imitation_learning")

        self.observation_space = spaces.Box(
            low=-2.0,
            high=2.0,
            shape=(12,),
            dtype=np.float32
        )

        self.num_directions = 8
        self.num_force_levels = 5
        self.action_space = Discrete(self.num_directions * self.num_force_levels)

        self.directions = [
            "Forward",
            "Backward",
            "Left",
            "Right",
            "Up",
            "Down",
            "Yaw Right",
            "Yaw Left"
        ]

        self.force_levels = [0, 25, 50, 75, 100]

        self.state = None

    def _getSubVel(self):
        response = requests.get(self.config["Velocity_URL"])
        response.raise_for_status()
        data = {k.lower(): v for k, v in response.json().items()}
        return data
    
    def _getSubRot(self):
        response = requests.get(self.config["Rotation_URL"])
        response.raise_for_status()
        data = {k.lower(): v for k, v in response.json().items()}
        return data
    
    def _setSubInputs(self):
        response = requests.post(self.config["Inputs_URL"], json=self.state)
        response.raise_for_status()
        data = {k.lower(): v for k, v in response.json().items()}
        return data
    
    def reset(self):
        print("{DEBUG} Resetting environment")
        self.state = None
        return self.state
