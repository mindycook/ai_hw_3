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
    cmap = cm.get_cmap('YlOrBr', n + 1)
    
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

    # Move pancakes around in the GUI
    # ***ENTER CODE HERE*** (5 lines) 
    
    # Get Sublist of Pancakes to be Flipped
    subcakes = pancakes[:p]
    
    # Delete Sublist from Main Pancakes List
    del pancakes[:p]
    
    # Reverse List of Pancakes
    pancakes.reverse()
    
    # Extend Pancake Sublist to End of Pancakes
    pancakes.extend(subcakes)
    
    # Reverse Pancakes Again to Correct Order
    pancakes.reverse()
       
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
    

    # Update the stack (which is separate from the graphics objects)
    # ***ENTER CODE HERE*** (2 lines)

    return stack

def cost(stack):
    '''Compute the cost h(stack) for a given stack of pancakes.
    Here, we define cost as the number of pancakes in the wrong position.'''
    # ***MODIFY CODE HERE*** (2 lines)
    h = 0
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

    # ***MODIFY CODE HERE*** (20-25 lines)
    cnt = 0

    print(f'searched {cnt} paths')
    print('solution:', '')
    status.setText("...search is complete")

def simulate(stack, path):
    '''Simulate the flipping of pancakes to determine the resulting stack.'''
    fakestack = stack.copy()  # make a copy so we don't actually change the real stack
    for action in path:
        try:
            p = int(action)  # how many pancakes are we trying to flip?
            for i in range(1, p // 2 + 1):
                fakestack[-i], fakestack[- (p - i + 1)] = fakestack[-(p - i + 1)], fakestack[-i]
        except:
            print("INVALID ACTION: Check code")

    return fakestack

if __name__ == "__main__":
    main(parser.parse_args())
