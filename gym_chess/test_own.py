import random
from gym_chess import ChessEnvV2

env = ChessEnvV2() # or ChessEnvV2

# current state
state = env.state
print(state,type(state))
# select a move and convert it into an action
moves = env.get_possible_moves(state=state, player="WHITE", attack=False)
move = random.choice(moves)
print(move)
# move = ((7, 1), (5, 0))
action = env.move_to_action(move)

# or select an action directly
# actions = env.possible_actions
# action = random.choice(actions)
# print(action)

# pass it to the env and get the next state
new_state, reward, done, info = env.step(action)
print(reward)