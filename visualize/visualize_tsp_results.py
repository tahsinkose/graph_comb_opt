import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(sltn):
	G = nx.Graph()
	#nodes = [i for i in range(0,len(sltn))]
	pos = {0: (0,0), 1: (-22.5,22.5), 2: (-7.5,22.5), 3: (7.5,22.5), 4: (22.5,22.5), 5: (-22.5,37.5), 6: (-7.5,37.5), 7: (7.5,37.5), 8: (22.5,37.5)}
	"""pos = {0: (0,5), 1: (10,10), 2: (10,15), 3: (-3,15), 4: (-10,5), 5: (0,-5), 
		   6: (0,-15), 7: (-10,-10), 8: (-10,-15), 9:(10,-10), 10: (20,-5), 11: (20,-10),
		   12: (20,5)}"""
	G.add_nodes_from(pos)
	for i in range(len(sltn)-1):
		G.add_edge(sltn[i],sltn[i+1])
	nx.draw(G, with_labels=True, font_weight='bold')
	plt.show()




if __name__=='__main__':
	solution = raw_input("")
	solution = [int(i) for i in solution.split(" ")]
	visualize_graph(solution)