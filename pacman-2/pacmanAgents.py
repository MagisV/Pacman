# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
import random
import game
import util
import api
from collections import deque

class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP

class GreedyAgent(Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)

def scoreEvaluation(state):
    return state.getScore()


class CornerSeekingAgent(Agent):
    
    def __init__(self):
        self.visited = set([])
        self.visited_corners = set([])
        self.curr_path = deque()

    def getAction(self, state):
        pacman = api.whereAmI(state)
        walls = api.walls(state)
        non_visited_corners = set(api.corners(state)) - self.visited_corners
        if not self.curr_path: # choose a new corner and compute path
            corner = random.choice(list(non_visited_corners))
            print("corner: ", corner)
            self.visited_corners.add(corner)
            to_x, to_y = get_non_wall_corner(corner)
            path = deque(find_path_to_point(pacman[0], pacman[1], to_x, to_y, walls, state))
            self.curr_path = path
        
        direction = self.curr_path.popleft()[2]
        print("direction: ", direction)

        # self.visited.add(pacman)

        return direction

def get_non_wall_corner(corner):
    x = corner[0]
    y = corner[1]
    
    if x == 0:
        x += 1
    else:
        x -= 1
    
    if y == 0:
        y += 1
    else:
        y -= 1
    
    return x, y

# bfs
def find_path_to_point(from_x, from_y, to_x, to_y, walls, state):
    visited = set()
    if (to_x, to_y) not in walls:
        queue = deque([(from_x, from_y, [])]) # queue of lists of (x, y, list of directions)
        while queue:
            x, y, path = queue.popleft()

            if (x, y) == (to_x, to_y):
                return path

            visited.add((x, y))

            moves = [(x+1, y, Directions.EAST), (x-1, y, Directions.WEST), (x, y+1, Directions.NORTH), (x, y-1, Directions.SOUTH)]
            
            for new_x, new_y, direction in moves:
                if is_valid(new_x, new_y, walls, state) and (new_x, new_y) not in visited:
                    new_path = path + [(x, y, direction)]
                    queue.append((new_x, new_y, new_path))
    
    return None # no path found

def is_valid(x, y, walls, state):
    width = state.getWalls().width
    height = state.getWalls().height
    is_valid = (0 <= x <= width) and (0 <= y <= height) and (x, y) not in walls
    return is_valid