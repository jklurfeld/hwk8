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
    states[state_name] = [None, state_neighbors]

print(states)


"""
Solution idea:
- pick the state with the most neighbors and color it and color all of its neighbors
- pick the next state with the most neighbors and color it and color all of its neighbors
- repeat until all states are colored
"""


def color_graph_simple(states) -> dict:
    # Color each node by simply going through the states from top of the dict to the bottom
    colors = ["blue", "red", "green", "yellow"]
    colorCounter = 0

    # Give states colors one after the other
    for state in states.keys():
        # set of colors of the neigbhors
        neighbor_colors = {states[neighbor][0] for neighbor in states[state][1] if states[neighbor][0] is not None}

        # color it the first color that no neighbor has
        colorCounter = 0    
        while colors[colorCounter] in neighbor_colors:
            colorCounter += 1
        
        # set the color of the state
        states[state][0] = colors[colorCounter]

        print(state, " is ", states[state][0])
    
    return states


def color_graph_most_connected(states) -> dict:
    # Color each node by going through the states from most connected to least connected
    colors = ["blue", "red", "green", "yellow"]
    colorCounter = 0

    # Sort the states by number of neighbors using bubble sort  
    for i in range(len(states)):
        for j in range(len(states)):
            if len(states[list(states.keys())[i]][1]) > len(states[list(states.keys())[j]][1]):
                states[list(states.keys())[i]], states[list(states.keys())[j]] = states[list(states.keys())[j]], states[list(states.keys())[i]]


    # Give states colors one after the other
    for state in states.keys():
        # set of colors of the neigbhors
        neighbor_colors = {states[neighbor][0] for neighbor in states[state][1] if states[neighbor][0] is not None}

        # color it the first color that no neighbor has
        colorCounter = 0    
        while colors[colorCounter] in neighbor_colors:
            colorCounter += 1
        
        # set the color of the state
        states[state][0] = colors[colorCounter]

        print(state, " is ", states[state][0])
    
    return states


def color_graph_breadth_first(states) -> dict:
    # Breadth first search inspired approach
    # Color each node by spreading out from a corner of the graph

    # Start from topmost westmost state
    start_state = 'Washington'

    colors = ["blue", "red", "green", "yellow"]
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
                    print(current_state, "is", color)
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
            print(state, "is", colors[0])

    return states

print(color_graph_breadth_first(states))