import numpy as np
from functools import reduce
# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
# ANSWER1 = True
# ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = None

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = None

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = None

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = None

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = None

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = None

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import *

# Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.


def bfs(graph, start, goal):
    queue= [[start]]
    extended_set= set({})
    while True:
        current_path= queue[0]
        end_node= current_path[-1]
        nodes= graph.get_connected_nodes(end_node)
        queue.remove(current_path)
        extended_set.add(end_node)
        nodes=[item for item in nodes if item not in extended_set]
        for extended_node in nodes:
            path= current_path+[extended_node]
            if extended_node== goal and graph.is_valid_path(path):
                return path
            queue.append(path)

# Once you have completed the breadth-first search,
# this part should be very simple to complete.


def dfs(graph, start, goal):
    queue= [[start]]
    extended_set= set({})
    while True:
        current_path= queue[0]
        end_node= current_path[-1]
        nodes= graph.get_connected_nodes(end_node)
        queue.remove(current_path)
        extended_set.add(end_node)
        nodes=[item for item in nodes if item not in extended_set]
        for extended_node in nodes:
            path= current_path+[extended_node]
            if extended_node== goal and graph.is_valid_path(path):
                return path
            queue.insert(0, path)

## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.


def hill_climbing(graph, start, goal):
    queue = [[start]]
    while True:
        current_path = queue[0]
        end_node = current_path[-1]
        nodes = graph.get_connected_nodes(end_node)
        queue.remove(current_path)
        nodes= [node for node in nodes if node not in current_path]
        nodes_heuristics=[]
        for node in nodes:
            nodes_heuristics.append(graph.get_heuristic(node, goal))
        nodes= [nodes[x] for x in (-np.array(nodes_heuristics)).argsort()]
        for extended_node in nodes:
            path = current_path + [extended_node]
            if extended_node == goal and graph.is_valid_path(path):
                return path
            queue.insert(0, path)

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the
## graph get_heuristic function, with lower values being better values.


def prouning(graph, goal, queue, k):
    if len(queue[0])== len(queue[-1]):
        nodes= [x[-1] for x in queue]
        nodes_heuristics = []
        for node in nodes:
            nodes_heuristics.append(graph.get_heuristic(node, goal))
        queue_sorted= [queue[x] for x in (np.array(nodes_heuristics)).argsort()]
        return queue_sorted[:k]
    else:
        return queue

def beam_search(graph, start, goal, beam_width):
    queue = [[start]]
    while True:
        current_path = queue[0]
        end_node = current_path[-1]
        nodes = graph.get_connected_nodes(end_node)
        queue.remove(current_path)
        nodes = [node for node in nodes if node not in current_path]
        for extended_node in nodes:
            path = current_path + [extended_node]
            if extended_node == goal and graph.is_valid_path(path):
                return path
            queue.append(path)
        queue= prouning(graph, goal, queue, beam_width)

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.


def path_length(graph, node_names):
    length=0
    for i in range(len(node_names))[:-1]:
        length+= graph.get_edge(node_names[i], node_names[i+1]).length
    return length


def branch_and_bound(graph, start, goal):
    queue = [[start]]
    queue_path= [0]
    goal_path=None
    goal_length= float('Inf')
    while True:
        current_path = queue[0]
        pathl= queue_path[0]
        end_node = current_path[-1]
        nodes = graph.get_connected_nodes(end_node)
        queue.remove(current_path)
        queue_path.pop(0)
        nodes = [node for node in nodes if node not in current_path]
        for extended_node in nodes:
            path = current_path + [extended_node]
            updated_pathl= pathl+ graph.get_edge(end_node, extended_node).length
            if extended_node == goal and graph.is_valid_path(path) and updated_pathl<goal_length:
                goal_path= path.copy()
                goal_length= updated_pathl
            elif extended_node is not goal:
                queue.insert(0, path)
                queue_path.insert(0, updated_pathl)
        if np.all(np.array(queue_path) > goal_length):
            return goal_path
        queue = [queue[x] for x in (np.array(queue_path)).argsort()]
        queue_path.sort()

def a_star(graph, start, goal):
    queue = [[start]]
    queue_path = [0]
    extended_set= set({})
    goal_path = None
    goal_length = float('Inf')
    while True:
        current_path = queue[0]
        pathl = queue_path[0]
        end_node = current_path[-1]
        nodes = graph.get_connected_nodes(end_node)
        extended_set.add(end_node)
        queue.remove(current_path)
        queue_path.pop(0)
        nodes = [node for node in nodes if node not in current_path]
        nodes = [node for node in nodes if node not in extended_set]
        for extended_node in nodes:
            path = current_path + [extended_node]
            updated_pathl = pathl + graph.get_edge(end_node, extended_node).length
            if extended_node == goal and graph.is_valid_path(path) and updated_pathl < goal_length:
                goal_path = path.copy()
                goal_length = updated_pathl
            elif extended_node is not goal:
                queue.insert(0, path)
                queue_path.insert(0, updated_pathl)
        if np.all(np.array(queue_path) > goal_length):
            return goal_path

        heus= []
        for d in queue:
            heus.append(graph.get_heuristic(d[-1], goal))
        pathes= np.array(queue_path)+ np.array(heus)
        indecis= pathes.argsort()
        queue = [queue[x] for x in indecis]
        queue_path= [queue_path[x] for x in indecis]

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    nodes= [node for node in graph.nodes if node is not goal]
    for node in nodes:
        path= a_star(graph, node, goal)
        if path_length(graph, a_star(graph, node, goal)) < graph.get_heuristic(node, goal):
            return False
    return True

def is_consistent(graph, goal):
    nodes = [node for node in graph.nodes if node is not goal]
    for node in nodes:
        node_nodes= [x for x in nodes if x is not node]
        for x in node_nodes:
            if path_length(graph, a_star(graph, node, x)) < abs(graph.get_heuristic(node, goal)- graph.get_heuristic(x, goal)):
                return False
    return True
HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
