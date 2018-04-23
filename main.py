from Games import *
from Agents import *
import matplotlib.pyplot as plt



env = HexPawn2(None, None)
print(env.board)
env.pawn_locations = [[(1,0),(0,1),(0,2)],[(2,0),(2,1),(2,2)]]
print(env.legal_actions(None))
