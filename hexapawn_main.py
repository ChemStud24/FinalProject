from Games import *
from Agents import *
import matplotlib.pyplot as plt



def plot_results(title,games,statistics,names,xlabel = 'Games Played'):
	# inputs:
	# title is the plot title
	# games is a list of number of games played so far at each data point
	# statistics is a list of lists of with each list recording different statistics
	# names is a list of strings that name the variables in 'statistics' for the plots
	
	SUBS = {2 : '21', 3 : '31', 4 : '22', 6 : '32'}
	subs = SUBS.get(len(statistics))

	plt.figure()
	plt.suptitle(title)

	i = 1
	for stats,name in zip(statistics,names):
		if subs is not None:
			plt.subplot(subs + str(i))
			i += 1
		plt.plot(games,stats)
		plt.xlabel(xlabel)
		plt.ylabel(name)
	plt.show()

if __name__ == '__main__':

	GAMES = 10
	EPISODES = 20
	SIZE = 3

	Carlos = Learner(HexaPawn)
	players = [Carlos, RandomAgent(HexaPawn)]
	game = HexaPawn(players, size = SIZE)

	print('0 1 2\n3 4 5\n6 7 8\n')
	board = [['B', 'B', 'B'],
			 ['*', 'W', '*'],
			 ['W', '*', 'W']]
	actions = HexaPawn.legal_actions(board, 'B')
	print(actions)
	board = HexaPawn.step(board, actions[1], 'B')
	print(board)

	# Carlos = Learner(HexaPawn)
	# players = [Carlos, RandomAgent(HexaPawn)]
	# game = TicTacToe(players, size = SIZE)

	# wins_first, draws_first, losses_first, wins_second, losses_second, draws_second = [],[],[],[],[],[]

	# for e in range(EPISODES):
	# 	# state,turn = game.initialize()
	# 	# print('Player: ', turn, ' is starting')
	# 	print('\nEpisode',e)

	# 	game.play(GAMES)

	# 	wins_first.append(Carlos.wins_first)
	# 	draws_first.append(Carlos.draws_first)
	# 	losses_first.append(Carlos.losses_first)
	# 	wins_second.append(Carlos.wins_second)
	# 	draws_second.append(Carlos.draws_second)
	# 	losses_second.append(Carlos.losses_second)

	# 	print('\nProgress:')
	# 	print('Playouts:',Carlos.PLAYS)
	# 	print('States Visited:',sum(Carlos.TREE.get(s)[1] for s in Carlos.TREE.keys()))
	# 	print('Unique States Visited:',len(Carlos.TREE.keys()))

	# 	print('\nReults:')
	# 	print('Wins:', wins_first[-1] + wins_second[-1])
	# 	print('Losses:',losses_first[-1] + losses_second[-1])
	# 	print('Draws:',draws_first[-1] + draws_second[-1])

	# plot_results('Monte Carlo vs. Random Agent',
	# 	list(range(GAMES,EPISODES*GAMES+GAMES,GAMES)),
	# 	[wins_first, draws_first, wins_second, draws_second],
	# 	['Wins as X', 'Draws as X', 'Wins as O', 'Draws as O'])

	# Carlos.save('Carlos.lrn')