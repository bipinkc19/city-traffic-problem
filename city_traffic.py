"""
Solution in python 3.6

Assumptions and conlcusions done to get the required answer

1. There are no cycles in the graph
2. If a node has only single connection then it a dead-end node,
   hence the maximum traffic to the node is:- sum of all node - population of the node
3. Node at the end of the graph has only one edge

Computation for every node:
We explore every possible vertices for maximum possible and when doing that
the whole graph is explored once at that process hence the comlexity is O(N)

Although it looks like here:-

for vertice in vertices:
	temp_vertices = vertices.copy()
		temp_vertices.remove(vertice)
		traffic, _ = get_population_of_sub_graph(node=node, exclude_nodes=temp_vertices, graph=graph)
		traffics.append(traffic)

like the complexity is raised to O(N^2) but we are exploring sub graphs of the node, hence
at the end of the loop we have only explored the whole graph once for the particular node


So, for when computing for every city the complexity is raised to O(N^2)

Hashing and storing the direction or weights of sub-nodes can be done but that too
will require O(N^2) complexity for exploring and storing the whole graph.
"""

from ast import literal_eval

def get_items_of_sub_graph(parents, graph):
	"""Returns the nodes within the nodes in question and then returns the last
	node value when no further child are there in the graph in a recurssive manner

	Recursion helps boil down the code to a minimal approach where we explore nodes
	from a parent node, then again nodes from the child nodes until the node has met 
	dead end, and finally returning all the nodes in the sub-graph seperated by a vertice/edge

	Parameters
	----------
	parents : list[int]
		parent nodes to discuss
	graph : dict
		graph data excluding the nodes with only one vertices as it helps identify
		dead-end nodes
	"""
	global all_nodes, exclude_items
	for parent in parents:
		# All nodes contains the nodes in that sub-graph
		all_nodes += [parent]
		try:
			children = graph[parent].copy()
			# Excluding items like parent or grand parent nodes
			children = list(set(children) - set(exclude_items))
			exclude_items.append(parent)
			
			# recusive call for exploring nodes within nodes
			get_items_of_sub_graph(children, graph)
		except KeyError:
			# As we have graph data excluding the nodes with only one vertices as it helps 
			# identify dead-end nodes, so in KeyError sigifies end of node flow
			pass
		

def get_population_of_sub_graph(node, exclude_nodes, graph):
	"""Function wrapping get_items_of_sub_graph() which uses global variables to prevent 
	variable mutation and summing the number of nodes in the sub-graph obtained from get_items_of_sub_graph()

	Parameters
	----------
	node : int
		the node in question to find the components of its sub-graph
	exclude_nodes : list[int]
		list of nodes to excludes which prevents us from dublication and helps
		choose the single vertex/edge whose sub-graph is to be processed
	graph : dict
		graph data excluding the nodes with only one vertices as it helps identify
		dead-end nodes

	Returns
	-------
	int, list[int]
		sum of the node's population, list of nodes int eh sub-graph
	"""
	# Delaring global variables needed for the recursion
	global all_nodes, exclude_items
	all_nodes, exclude_items = [], exclude_nodes
	
	# Processing the subgraph
	get_items_of_sub_graph([node], graph)
	
	# Removing self node from the sub-graph as it doesn't count in traffic
	all_nodes.remove(node)
	all_nodes_except_self = all_nodes.copy()
	# Deleting golabl variables for preventing future conflicts
	del all_nodes, exclude_items
	
	return sum(all_nodes_except_self), all_nodes_except_self 


def CityTraffic(input):
	"""Returns the highest possible traffic in every city road (maximum possible edge of every node)

	Parameters
	----------
	input : list[str]
		raw input exampe format ["1:[5]", "4:[5]"]

	Returns
	-------
	dict
		maximum possible traffic for every city in ascending order of city
	"""
	# Parsing the raw input to pytho dictionary
	graph_org = {int(i.split(":")[0]): literal_eval(i.split(":")[1]) for i in input}
	# Removing nodes with only one connections as these are dead-end nodes og the graph
	graph = {k:v for k, v in graph_org.items() if len(v)>1}
	
	highest_traffic = {}
	# Looping through every node for finding its maximum traffic
	for node in graph_org.keys():
		sum_of_nodes = sum(set(sum(graph_org.values(), [])))
		vertices = graph_org[node]

		# If the node has only one connection then the node is a dead-end node with one edge
		# hence the maximum traffic would be population of all the nodes except itself
		if len(vertices) == 1:
			highest_traffic[node] = sum_of_nodes - node
			continue

		# If a node has more then one edge then we should check the maximum population
		# possible in every edge to fing the maximum population in the node
		# By excluding other edge/vertices we can get all the nodes connected to that node
		# through that vertice/edge
		# Hence, checking through every vertice/edge then finding the maximum among them 
		traffics = []
		for vertice in vertices:
			# Preventing mutation when removing the vertice in checking
			# so in exclude list all other vertices are included except the one in question
			# by excluding all the nodes except the node in question we get the vertice in question
			temp_vertices = vertices.copy()
			temp_vertices.remove(vertice)
			traffic, _ = get_population_of_sub_graph(node=node, exclude_nodes=temp_vertices, graph=graph)
			traffics.append(traffic)
		
		highest_traffic[node] = max(traffics)
	
	# Return sorted according to keys
	return dict(sorted(highest_traffic.items()))

if __name__ == "__main__":
	assert CityTraffic(["1:[5]", "4:[5]", "3:[5]", "5:[1,4,3,2]", "2:[5,15,7]", "7:[2,8]", "8:[7,38]", "15:[2]", "38:[8]"]) == {
		1:82, 2:53, 3:80, 4:79, 5:70, 7:46, 8:38, 15:68, 38:45
	}
	assert CityTraffic(["1:[5]", "2:[5]", "3:[5]", "4:[5]", "5:[1,2,3,4]"]) == {
		1:14, 2:13, 3:12, 4:11, 5:4
	}
	assert CityTraffic(["1:[5]", "2:[5,18]", "3:[5,12]", "4:[5]", "5:[1,2,3,4]", "18:[2]", "12:[3]"]) == {
		1:44, 2:25, 3:30, 4:41, 5:20, 12:33, 18:27
	}
	print("Test succesful")
