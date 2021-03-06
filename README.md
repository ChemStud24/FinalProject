# FinalProject
ESE650: Learning in Robotics Final Project

Reinforcement Learning by Self-Play

========================================================================

Games.py contains classes for Game objects with the following methods:

__init__(self, params) : instantiates the game

legal_actions(self, state = curr) : returns the legal actions of the (current) state of the game

reward(self, state = curr) : returns a reward for the current state, typically 1 for win, -1 for loss, 0 for draw.  If the state is not terminal, returns None.

step(self, action, state = curr) : steps the game with action to the next state (from the current state)

play(self) : queries actions from the players and calls self.step() repeatedly until done

display(self, state = curr) : prints a representation of the (currernt) state by calling self.__str__()

__str__(self, state = curr) : returns a string representation of the (current) state

ELIMINATED:

done(self, state = curr) : returns True if the (current) state is a terminal state

========================================================================

Agents.py contains classes for Agent objects with the following methods:

__init__(self, params) : instantiates the agent

action(self, state, legal_actions) : returns a legal action given the state of the game

save(self, filename) : save's the agent's internal table, heuristic, etc. used for choosing actions

load(self, filename) : load's the agent's memory/experience from a file that was made by calling agent.save()

ELIMINATED:

update(self, state, action, reward) : updates the agent's internal decision making given the reward