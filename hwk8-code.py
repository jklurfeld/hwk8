# Names: Jessica Klurfeld and Michelle Lawson
# Peers: N/A
# References: Lesly Gonzalez Herrera’s States.csv.csv file from the #technews channel

# This algorithm finds the greedy method to color a graph so that no neighboring states have the same color.

import csv
from collections import deque # for breadth first coloring
    
with open('States.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader, None)
    state_data = list(reader)

states = {}



# storing states in dictionary withkeys of state names and  values of color and neighbors
for i in range(len(state_data)):
    state_name = state_data[i][0]
    state_neighbors = state_data[i][1].split(',')
    state_neighbors = [x.strip(' ') for x in state_neighbors]
    if state_neighbors[0] == 'N/A':
        state_neighbors = []
    state_num_neighbors = int(state_data[i][2])
    states[state_name] = [None, state_neighbors, state_num_neighbors]


def color_graph_breadth_first(states) -> dict:
    """
    Colors each state in the graph using a breadth-first search inspired approach, such that no two neighboring states are the same color.

    :param states: (dict) A dictionary where each key is a state and its value is a list containing its color (initially None), a list of its neighboring states, and the number of neighbors.

    :return: (dict) A dictionary with the updated states where each key is a state and its value is a list containing its color and a list of its neighboring states, and the number of neighbors.
    """
    # Breadth first search inspired approach
    # Color each node by spreading out from a corner of the graph

    # Start from topmost westmost state
    start_state = 'Washington'

    colors = ["blue", "pink", "green", "yellow"]
    visited = set()
    queue = deque()

    queue.append(start_state)

    while queue:
        current_state = queue.popleft()
        visited.add(current_state)

        try:
            # Determine the color for the current state

            neighbor_colors = {states[neighbor][0] for neighbor in states[current_state][1] if states[neighbor][0] is not None}
            color_assigned = False

            for color in colors:
                if color not in neighbor_colors:
                    states[current_state][0] = color
                    color_assigned = True
                    # print(current_state, "is", color)
                    break

            if not color_assigned: # raise an error if coloring failed
                raise ValueError(f"Unable to assign color to state {current_state}")

        except ValueError as e:
            print(f"Error occurred: {e}")

        # add all unvisited neighbors to the queue
        for neighbor in states[current_state][1]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
    
    # Color isolated states
    # if an error occurred, then it just colors it blue at the end
    for state in states.keys():
        if states[state][0] is None: # if a state is not yet colored
            states[state][0] = colors[0] # give it the first color because it has no neighbors
            # print(state, "is", colors[0])

    return states


def color_graph_most_neighbors(states):
    """
    Starting from the state with the most neighbors, colors each state in the graph such that no two neighboring states are the same color.

    :param states: (dict) A dictionary where each key is a state and its value is a list containing its color (initially None), a list of its neighboring states, and the number of neighbors.
    
    :return: (dict) A dictionary with the updated states where each key is a state and its value is a list containing its color and a list of its neighboring states, and the number of neighbors.
    """
    # colors a graph by coloring the states with the most neighbors first (and all of their neighbors)
    # note: does not take into account whether those neighbors have already been colored, only cares about the number of neighbors

    colors = ["blue", "pink", "green", "yellow"]
    visited = set()
    queue = deque()

    # visits the 48 contiguous United States first
    while (len(visited) != 48):
        # find the state with the most neighbors that hasn't already been visited
        max = 0
        for state in states.keys():
            if states[state][2] > max and state not in visited:
                max = states[state][2]
                maxState = state

        # color the maxState and its neighbors, mark it and all of its neighbors as visited
        queue.append(maxState)
        for neighbor in states[maxState][1]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
        
        # color in the max state and its neighbors
        while queue:
            current_state = queue.popleft()
            visited.add(current_state)
            try:
                # Determine the color for the current state
                neighbor_colors = {states[neighbor][0] for neighbor in states[current_state][1] if states[neighbor][0] is not None}
                color_assigned = False

                for color in colors:
                    if color not in neighbor_colors:
                        states[current_state][0] = color
                        color_assigned = True
                        # print(current_state, "is", color)
                        break

                if not color_assigned: # raise an error if coloring failed
                    raise ValueError(f"Unable to assign color to state {current_state}")

            except ValueError as e:
                print(f"Error occurred: {e}")

    # color isolated states
    for state in states.keys():
        if states[state][0] is None: # if a state is not yet colored
            states[state][0] = colors[0] # give it the first color because it has no neighbors
            # print(state, "is", colors[0])

    return states

print(color_graph_breadth_first(states))