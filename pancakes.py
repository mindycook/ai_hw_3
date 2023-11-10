# pancakes.py
# Flipping pancakes with greedy best-first search (GBFS).

import argparse
from graphics import *
from matplotlib import cm
import pdb
from queue import PriorityQueue
import random
import time

parser = argparse.ArgumentParser(description="Use greedy best-first search (GBFS) to optimally flip a stack of pancakes")
parser.add_argument('-n', '--num', metavar='pancakes', type=int, help="number of pancakes", default=8)
parser.add_argument('--seed', type=int, help="seed for randomly arranging pancakes initially")

def main(args):
    # Parse inputs
    n = args.num  # number of pancakes
    stack = list(range(n))
    if args.seed is not None:  # randomly shuffle the pancakes initially
        random.shuffle(stack)

    # Make the graphical user interface
    gui = guisetup(stack)

    # Use the graphical user interface
    while True:
        key = gui.checkKey()
        if key:
            if key == "Escape":  # quit the program
                break
            elif key == 'd':  # debug the program
                pdb.set_trace()
            elif key == 'g':  # run greedy best-first search
                path = gbfs(gui, stack)
            elif key in [str(i) for i in range(1, n + 1)]:  # manually flip some of the pancakes
                flip(gui, stack, int(key))

    gui.close()

def guisetup(stack):
    '''Create graphical user interface for a stack of n pancakes.'''
    n = len(stack)  # number of pancakes in the stack
    thickness = 12  # thickness of each pancake, in pixels
    margin = 40 # Space between wall and pancake on each side
    wid = margin * 2 + 30 * max(n + 1, 9)  # each successive pancake gets 30 px wider
    hei = margin * 2 + n * thickness  # top/bottom margins of 40 px + 12 px per pancake
    gui = GraphWin("Pancakes", wid, hei)

    cx = wid / 2  # center of width
    cmap = cm.get_cmap('YlOrBr', n + 1) # YlOrBr
    
    # Change Background Color of GUI
    gui.setBackground("#dee2e6")
    

    # Draw pancakes
    # ***ENTER CODE HERE*** (10 lines)
    for i in range(n): # For every pancake
        # Create Pancake Object
        pancake = Line(Point(margin + (15 * i), hei - margin - (thickness*i)), Point(wid - (margin + 15 * i), hei - margin - (thickness*i)))
        # Set Thickness of Pancake
        pancake.setWidth(thickness)
        # Draw Pancake on Board
        pancake.draw(gui)
        # Get Unformatted Color Values from Color Map (MatPlotLib)
        color_array = cmap(n-i)
        # Formatted RGB Color Values
        r, g, b = int(color_array[0] * 255), int(color_array[1] * 255), int(color_array[2] * 255)
        # Convert RGB Value to Hex Value
        pancakecolor = color_rgb(r, g, b)
        # Set Pancake to Color of Hex Value
        pancake.setFill(pancakecolor)
        
    # Before Adding Text Object, Reverse Order of Pancakes
    gui.items.reverse()

    # Add text objects for instructions and status updates
    instructions = Text(Point(10, hei - 12), "Press a # to flip pancakes, 'g' to run GBFS, Escape to quit")
    instructions._reconfig("anchor", "w")
    instructions.setSize(8)
    instructions.draw(gui)

    status = Text(Point(cx, 20), "")
    status._reconfig("anchor", "center")
    status.setSize(12)
    status.draw(gui)

    # Return gui object
    return gui

def flip(gui, stack, p):
    '''Flip p pancakes in an ordered stack.'''
    # print("Flipping", p, "pancakes" if p > 1 else "pancake")

    # Get graphics objects from GUI
    obj = gui.items
    # Pancakes is a List of Line Objects
    pancakes = obj[:-2]
    # 2nd Last Text Object from GUI
    anchor = obj[-2]
    # Last Text Object from GUI
    status = obj[-1]
    
    # Update status text on GUI
    status.setText(f"Flipping {p} pancake{'s' if p > 1 else ''}")
    
    # Create a Copy of Pancakes for Reference to Find Difference
    original_cakes = pancakes[:]

    # Move pancakes around in the GUI --------------------------
    
    # Get Sublist of Pancakes to be Flipped
    subcakes = pancakes[:p]
    substack = stack[:p]
    
    # Delete Sublist from Main Pancakes List
    del pancakes[:p]
    del stack[:p]
    
    # Reverse List of Pancakes
    pancakes.reverse()
    stack.reverse()
    
    # Extend Pancake Sublist to End of Pancakes
    pancakes.extend(subcakes)
    stack.extend(substack)
    
    # Reverse Pancakes Again to Correct Order
    pancakes.reverse()
    stack.reverse()
       
    # Thickness of Pancake
    thickness = pancakes[0].config['width']  # may be a helpful variable :)
    
    # Draw Updated Pancakes
    for i in range(len(pancakes)):
        # Find Difference of Length (Indices) each Pancake Shifted
        difference = i - original_cakes.index(pancakes[i])
        # Move Pancake Line Objects to Updated Position
        original_cakes[i].move(0, difference * thickness * -1)
        
    # Update Items in GUI
    gui.items = pancakes # List of Rearranged Pancakes
    gui.items.append(anchor) # First Text Object
    gui.items.append(status) # Second Text Object
    
    # Return Updated Stack
    return stack

def cost(stack):
    '''Compute the cost h(stack) for a given stack of pancakes.
    Here, we define cost as the number of pancakes in the wrong position.'''
   
    # ***MODIFY CODE HERE*** (2 lines)
    h = 0 # Number of Pancakes in Incorrect Position
    
    # For Every Pancake in Stack
    for i in range(len(stack)):
        # If Pancake is in Incorrect Position (Index)
        if stack[i] != i:
            # Increment Number of Incorrect Pancakes
            h += 1
    
    # Return Cost
    return h

def gbfs(gui, stack):
    '''Run greedy best-first search on a stack of pancakes and return the solution path.'''
    print("Running greedy best-first search...")

    # Get graphics objects from GUI
    obj = gui.items
    pancakes = obj[:-2]
    status = obj[-1]

    # Update status text on GUI
    status.setText(f"Running greedy best-first search...")
    time.sleep(0.5)
   
    # Count # of Iterations / Paths Searched
    cnt = 0
    
    # Initialze Desired Solution Path to Compares States to
    desired_solution = list(range(len(stack))) # [0, 1, 2, 3, 4, 5, ..., n-1]
    
    # Initialize Priority Queue
    pq = PriorityQueue()
    
    # Initialize Cost to Nodes
    cost_to_node = {}
    
    # Initialize Backpointers
    backpointers = {}
    
    # Add Starting State to Priority Queue
    pq.put((cost(stack), stack))
    
    # Add Starting State to List of Visited Nodes (Cost)
    cost_to_node.update({" ".join(map(str, stack)) : 0})
    
    # Loop Until Solution Found
    while True:
        
        # If Queue is Empty, Return Failure
        if pq.qsize == 0:
            solution = "None found... :("
            break
        
        # Pop Front Node (Stack) from PQ
        front = pq.get()[1]
        
        # Check if Popped Node Contains Goal
        if front == desired_solution:
            break
            
        # Start Expanding from Front with Each Available Action (# of Pancakes Flipped)
        for flip in range(2, len(stack) + 1):
         
            # Increment Count
            cnt += 1
            
            # Determine Child Node (Returns Updated Stack)
            child = simulate(front, flip)
                    
            # Lists (Stacks) cannot be Elements of a Dictionary, so Convert the Lists to Strings
            child_str = " ".join(map(str, child))
            front_str = " ".join(map(str, front))
            
            # Determine Cost of Child Node
            child_cost = cost(child)
            
            # Only Add Node to PQ if Child has NOT been Visited
            if cost_to_node.get(child_str) == None:
                # Add Child to PQ
                pq.put((child_cost, child))
                # Update Cost IN TERMS OF PATH COST (FLIPS)
                cost_to_node.update({child_str : flip})
                # Update Backpointer
                backpointers.update({child_str : front_str})
    
    # ------------------------------------

    # Initialize priority queue, cost to node, backpointers
    pq = PriorityQueue()
     # the previous stack b4 changing
    backpointers = {stack : None}

    # Add starting node to priority queue
    pq.put((cost(stack), stack))

    # Loop until solution is found or queue is empty
    flag = False
    while not pq.empty():
        # be sure to avoid repeating states
        node = pq.get() # Pop the first node off the queue
        print(f'Searching {node[1]}{node[0]}  | ', end="")

        # Check if we have reached the goal
        if node[0] == 0:
            flag = True
            break

        # For each available action (8 pancakes)
        for i in range(len(stack)):
            # Determine the cost of the child node
            child = flip(gui, stack, i+1)
            new_cost = cost(child)

            # If the child gives a lower heuristic,
            if cost(child) == 0 or cost(child) < node[0]:
                pq.put((cost(child), child))
                backpointers.append({child : i+1})
            # Put it on the queue




    print(f'searched {cnt} paths')
    print(f'solution: {displaySolution(backpointers, cost_to_node)}')
    status.setText("...search is complete")

def simulate(stack, path):
    '''Simulate the flipping of pancakes to determine the resulting stack.'''
    # Reverse Fake Stack, as This Code Flips the Opposite End
    fakestack = stack.copy()  # make a copy so we don't actually change the real stack
    # Reverse Fake Stack, as This Code Flips the Opposite End
    fakestack.reverse()

    for i in range(1, path // 2 + 1):
        fakestack[-i], fakestack[- (path - i + 1)] = fakestack[-(path - i + 1)], fakestack[-i]
    '''
    fakestack = stack.copy()  # make a copy so we don't actually change the real stack
    for action in path:
        try:
            p = int(action)  # how many pancakes are we trying to flip?
            for i in range(1, p // 2 + 1):
                fakestack[-i], fakestack[- (p - i + 1)] = fakestack[-(p - i + 1)], fakestack[-i]
        except:
            print("INVALID ACTION: Check code")
    '''

    # Reverse Again Before Sending Back
    fakestack.reverse()

    return fakestack

def displaySolution(backpointers, cost_to_node):
    # Define Start of Backpointing Stack Solution
    prev = '0 1 2 3 4 5 6 7'
           
    # Initialize Path Solution
    path = []
    
    # Append Backpointer Values to Solution List
    while prev != None:
        # Cost is None at End, so Remove after Loop
        path.append(cost_to_node.get(prev))
        # Update Prev
        prev = backpointers.get(prev)
        
    # Cost of Beginning State is None, so Remove
    del path[-1]
        
    # Reverse Solution List
    path.reverse()
    
    # Return Solution
    return " ".join(map(str, path))

if __name__ == "__main__":
    main(parser.parse_args())
