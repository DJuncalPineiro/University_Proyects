# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from array import array
from cmath import atan
from re import S
from xmlrpc.client import FastMarshaller
import util
import numpy as np
from game import Actions as ac
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters

class NullGraphics:
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

    def ghost_close(self, ghost_dist):
        if True in ghost_dist: return True
        else: return False 
    
    def printLineData(self,gameState, last=False):
        """
        Input:
            gameState
        Output:
            All attributes in state
        """
       
        #Change this to the real action if you want correctly the .arff dataset
        
        action = self.chooseAction(gameState)
        wall_ahead = False
        direction = gameState.data.agentStates[0].getDirection()
        
        legal = gameState.getLegalPacmanActions()
        
        if action == "Stop":
            wall_ahead = True
             
        ghost_distance=gameState.data.ghostDistances
        ghost_distance=list(filter(None,ghost_distance))

        min_distance=min(ghost_distance)
        
        index=gameState.data.ghostDistances.index(min_distance)
        
        ghost_pos1=gameState.getGhostPositions()[index][0]
        ghost_pos2=gameState.getGhostPositions()[index][1]
        ghost_list = gameState.getLivingGhosts()
        vector = (ghost_pos1-gameState.getPacmanPosition()[0], ghost_pos2-gameState.getPacmanPosition()[1])
        ghost_in_action1=ghost_in_action2=ghost_in_action3=ghost_in_action4=False


        if vector[0]==-1 and (-1<=vector[1] or vector[1]<=1):
            ghost_in_action1=True
        elif vector[0]==1 and (-1<=vector[1] or vector[1]<=1):
            ghost_in_action2=True
        elif vector[1]==-1 and (-1<=vector[0] or vector[0]<=1):
            ghost_in_action3=True
        elif vector[1]==-1 and (-1<=vector[0] or vector[0]<=1):
            ghost_in_action4=True
        else:
            ghost_in_action1=ghost_in_action2=ghost_in_action3=ghost_in_action4=False

        ghost_list = [ghost_in_action1,ghost_in_action2,ghost_in_action3,ghost_in_action4]
        ghost_state = [gameState.getLivingGhosts()[1],gameState.getLivingGhosts()[2],gameState.getLivingGhosts()[3],gameState.getLivingGhosts()[4]]
        ghost_is_close = self.ghost_close(ghost_list)

        module = round((vector[0]**2+vector[1]**2)**0.5,2)
        epsilon = 1e-8
        angle = round(np.rad2deg(np.arctan2(vector[1],(vector[0]+epsilon))),2)
        count = ghost_state.count(True)
       
        #Datos totales recogidos: score, pacman pos, module, angle, pacman direcc, wall_ahead, ghost pos, living ghost, ghost count, ghost dist, closest ghost pos,ghost_in_action, ghost is close,  action  
        data = [gameState.getScore(),
                gameState.getPacmanPosition()[0],
                gameState.getPacmanPosition()[1],
                module,
                angle,
                direction,
                wall_ahead, 
                gameState.getGhostPositions()[0][0], 
                gameState.getGhostPositions()[0][1],
                gameState.getGhostPositions()[1][0],
                gameState.getGhostPositions()[1][1],
                gameState.getGhostPositions()[2][0], 
                gameState.getGhostPositions()[2][1],
                gameState.getGhostPositions()[3][0], 
                gameState.getGhostPositions()[3][1], 
                gameState.getLivingGhosts()[1], 
                gameState.getLivingGhosts()[2], 
                gameState.getLivingGhosts()[3], 
                gameState.getLivingGhosts()[4],
                count, 
                gameState.data.ghostDistances[0],
                gameState.data.ghostDistances[1],
                gameState.data.ghostDistances[2],
                gameState.data.ghostDistances[3],
                ghost_pos1,ghost_pos2,ghost_in_action1,ghost_in_action2,ghost_in_action3,ghost_in_action4,ghost_is_close,action]
        #Change last line to complete the circuit
        if last == True:
            data[1] = ghost_pos1
            data[2] = ghost_pos2
            data[3]=0.0
            data[15]=data[16]=data[17]=data[18] = False
            data[19]=data[20]=data[21]=data[22]=data[23]=data[24]=data[25] = 0
            data[-2]=data[-3]=data[-4]=data[-5]=data[-6]=False
            data[-1] = "Stop"


        return data 


from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
        
    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move
        
class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST


from data_modification_old import change_data_1
from data_modification import change_data_2

from joblib import load





class Agent_pr1(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        ## CHANGE PATH TO MODEL
        self.model=load("./models/models_practica1/GaussianNB_top.joblib")

        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
    
    def ghost_close(self, ghost_dist):
        if True in ghost_dist: return True
        else: return False 

    def printLineData(self,gameState, last=False):
        """
        Input:
            gameState
        Output:
            All attributes in state
        """
       
        #Change this to the real action if you want correctly the .arff dataset
        action = "East"


        direction = gameState.data.agentStates[0].getDirection()
        legal = [a for a in gameState.getLegalPacmanActions()]
        
        if direction not in legal:
            wall_ahead = True
        else: 
            wall_ahead = False
             
        ghost_distance=gameState.data.ghostDistances
        ghost_distance=list(filter(None,ghost_distance))

        min_distance=min(ghost_distance)
        
        index=gameState.data.ghostDistances.index(min_distance)
        
        ghost_pos1=gameState.getGhostPositions()[index][0]
        ghost_pos2=gameState.getGhostPositions()[index][1]
        ghost_list = gameState.getLivingGhosts()
        vector = (ghost_pos1-gameState.getPacmanPosition()[0], ghost_pos2-gameState.getPacmanPosition()[1])
        ghost_in_action1=ghost_in_action2=ghost_in_action3=ghost_in_action4=False


        if vector[0]==-1 and (-1<=vector[1] or vector[1]<=1):
            ghost_in_action1=True
        elif vector[0]==1 and (-1<=vector[1] or vector[1]<=1):
            ghost_in_action2=True
        elif vector[1]==-1 and (-1<=vector[0] or vector[0]<=1):
            ghost_in_action3=True
        elif vector[1]==-1 and (-1<=vector[0] or vector[0]<=1):
            ghost_in_action4=True
        else:
            ghost_in_action1=ghost_in_action2=ghost_in_action3=ghost_in_action4=False

        ghost_list = [ghost_in_action1,ghost_in_action2,ghost_in_action3,ghost_in_action4]
        ghost_state = [gameState.getLivingGhosts()[1],gameState.getLivingGhosts()[2],gameState.getLivingGhosts()[3],gameState.getLivingGhosts()[4]]
        ghost_is_close = self.ghost_close(ghost_list)

        module = round((vector[0]**2+vector[1]**2)**0.5,2)
        epsilon = 1e-8
        angle = round(np.rad2deg(np.arctan2(vector[1],(vector[0]+epsilon))),2)
        count = ghost_state.count(True)
       
        #Datos totales recogidos: score, pacman pos, module, angle, pacman direcc, wall_ahead, ghost pos, living ghost, ghost count, ghost dist, closest ghost pos,ghost_in_action, ghost is close,  action  
        data = [gameState.getScore(),
                gameState.getPacmanPosition()[0],
                gameState.getPacmanPosition()[1],
                module,
                angle,
                gameState.data.agentStates[0].getDirection(),
                wall_ahead, 
                gameState.getGhostPositions()[0][0], 
                gameState.getGhostPositions()[0][1],
                gameState.getGhostPositions()[1][0],
                gameState.getGhostPositions()[1][1],
                gameState.getGhostPositions()[2][0], 
                gameState.getGhostPositions()[2][1],
                gameState.getGhostPositions()[3][0], 
                gameState.getGhostPositions()[3][1], 
                gameState.getLivingGhosts()[1], 
                gameState.getLivingGhosts()[2], 
                gameState.getLivingGhosts()[3], 
                gameState.getLivingGhosts()[4],
                count, 
                gameState.data.ghostDistances[0],
                gameState.data.ghostDistances[1],
                gameState.data.ghostDistances[2],
                gameState.data.ghostDistances[3],
                ghost_pos1,ghost_pos2,ghost_in_action1,ghost_in_action2,ghost_in_action3,ghost_in_action4,ghost_is_close,action]
        #Change last line to complete the circuit
        if last == True:
            data[1] = ghost_pos1
            data[2] = ghost_pos2
            data[3]=0.0
            data[15]=data[16]=data[17]=data[18] = False
            data[19]=data[20]=data[21]=data[22]=data[23]=data[24]=data[25] = 0
            data[-2]=data[-3]=data[-4]=data[-5]=data[-6]=False
            data[-1] = "Stop"


        return data  

    def printInfo(self, gameState):
        print "---------------- TICK ", self.countActions, " --------------------------"
        # Dimensiones del mapa
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print "Width: ", width, " Height: ", height
        # Posicion del Pacman
        print "Pacman position: ", gameState.getPacmanPosition()
        # Acciones legales de pacman en la posicion actual
        print "Legal actions: ", gameState.getLegalPacmanActions()
        # Direccion de pacman
        print "Pacman direction: ", gameState.data.agentStates[0].getDirection()
        # Numero de fantasmas
        print "Number of ghosts: ", gameState.getNumAgents() - 1
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        print "Living ghosts: ", gameState.getLivingGhosts()
        # Posicion de los fantasmas
        print "Ghosts positions: ", gameState.getGhostPositions()
        # Direciones de los fantasmas
        print "Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Distancia de manhattan a los fantasmas
        print "Ghosts distances: ", gameState.data.ghostDistances
        # Puntos de comida restantes
        print "Pac dots: ", gameState.getNumFood()
        # Distancia de manhattan a la comida mas cercada
        print "Distance nearest pac dots: ", gameState.getDistanceNearestFood()
        # Paredes del mapa
        print "Map:  \n", gameState.getWalls()
        # Puntuacion
        print "Score: ", gameState.getScore()

       
        
    def chooseAction(self, gameState):
        self.countActions = self.countActions + 1
        data=self.printLineData(gameState)
        legal=gameState.getLegalActions(0)
        encoded_data,decoder=change_data_1(data)
        prediction=self.model.predict([encoded_data])
        action=decoder.inverse_transform(prediction)
        action=action[0]

        print("Predicted action: ",action)

        if action in legal and action != "Stop":
            return action
        else:
            move_random = random.randint(0, 3)
            move=Directions.STOP
            if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
            if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
            if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
            if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        
            return move


class Agent_pr2(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        ## CHANGE PATH TO MODEL
        self.model_name = ""
        

        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
    
    def ghost_close(self, ghost_dist):
        if True in ghost_dist: return True
        else: return False 

    def printLineData(self,gameState, last=False):
        """
        Input:
            gameState
        Output:
            All attributes in state
        """
       
        #Change this to the real action if you want correctly the .arff dataset
        
        action = "East"
        
        direction = gameState.data.agentStates[0].getDirection()
        legal = [a for a in gameState.getLegalPacmanActions()]
        
        if direction not in legal:
            wall_ahead = True
        else: 
            wall_ahead = False
             
        ghost_distance=gameState.data.ghostDistances
        ghost_distance=list(filter(None,ghost_distance))

        min_distance=min(ghost_distance)
        
        index=gameState.data.ghostDistances.index(min_distance)
        
        ghost_pos1=gameState.getGhostPositions()[index][0]
        ghost_pos2=gameState.getGhostPositions()[index][1]
        ghost_list = gameState.getLivingGhosts()
        vector = (ghost_pos1-gameState.getPacmanPosition()[0], ghost_pos2-gameState.getPacmanPosition()[1])
        ghost_in_action1=ghost_in_action2=ghost_in_action3=ghost_in_action4=False


        if vector[0]==-1 and (-1<=vector[1] or vector[1]<=1):
            ghost_in_action1=True
        elif vector[0]==1 and (-1<=vector[1] or vector[1]<=1):
            ghost_in_action2=True
        elif vector[1]==-1 and (-1<=vector[0] or vector[0]<=1):
            ghost_in_action3=True
        elif vector[1]==-1 and (-1<=vector[0] or vector[0]<=1):
            ghost_in_action4=True
        else:
            ghost_in_action1=ghost_in_action2=ghost_in_action3=ghost_in_action4=False

        ghost_list = [ghost_in_action1,ghost_in_action2,ghost_in_action3,ghost_in_action4]
        ghost_state = [gameState.getLivingGhosts()[1],gameState.getLivingGhosts()[2],gameState.getLivingGhosts()[3],gameState.getLivingGhosts()[4]]
        ghost_is_close = self.ghost_close(ghost_list)

        module = round((vector[0]**2+vector[1]**2)**0.5,2)
        epsilon = 1e-8
        angle = round(np.rad2deg(np.arctan2(vector[1],(vector[0]+epsilon))),2)
        count = ghost_state.count(True)
       
        #Datos totales recogidos: score, pacman pos, module, angle, pacman direcc, wall_ahead, ghost pos, living ghost, ghost count, ghost dist, closest ghost pos,ghost_in_action, ghost is close,  action  
        data = [gameState.getScore(),
                gameState.getPacmanPosition()[0],
                gameState.getPacmanPosition()[1],
                module,
                angle,
                direction,
                wall_ahead, 
                gameState.getGhostPositions()[0][0], 
                gameState.getGhostPositions()[0][1],
                gameState.getGhostPositions()[1][0],
                gameState.getGhostPositions()[1][1],
                gameState.getGhostPositions()[2][0], 
                gameState.getGhostPositions()[2][1],
                gameState.getGhostPositions()[3][0], 
                gameState.getGhostPositions()[3][1], 
                gameState.getLivingGhosts()[1], 
                gameState.getLivingGhosts()[2], 
                gameState.getLivingGhosts()[3], 
                gameState.getLivingGhosts()[4],
                count, 
                gameState.data.ghostDistances[0],
                gameState.data.ghostDistances[1],
                gameState.data.ghostDistances[2],
                gameState.data.ghostDistances[3],
                ghost_pos1,ghost_pos2,ghost_in_action1,ghost_in_action2,ghost_in_action3,ghost_in_action4,ghost_is_close,action]
        #Change last line to complete the circuit
        if last == True:
            data[1] = ghost_pos1
            data[2] = ghost_pos2
            data[3]=0.0
            data[15]=data[16]=data[17]=data[18] = False
            data[19]=data[20]=data[21]=data[22]=data[23]=data[24]=data[25] = 0
            data[-2]=data[-3]=data[-4]=data[-5]=data[-6]=False
            data[-1] = "Stop"


        return data  

    def printInfo(self, gameState):
        print "---------------- TICK ", self.countActions, " --------------------------"
        # Dimensiones del mapa
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print "Width: ", width, " Height: ", height
        # Posicion del Pacman
        print "Pacman position: ", gameState.getPacmanPosition()
        # Acciones legales de pacman en la posicion actual
        print "Legal actions: ", gameState.getLegalPacmanActions()
        # Direccion de pacman
        print "Pacman direction: ", gameState.data.agentStates[0].getDirection()
        # Numero de fantasmas
        print "Number of ghosts: ", gameState.getNumAgents() - 1
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        print "Living ghosts: ", gameState.getLivingGhosts()
        # Posicion de los fantasmas
        print "Ghosts positions: ", gameState.getGhostPositions()
        # Direciones de los fantasmas
        print "Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Distancia de manhattan a los fantasmas
        print "Ghosts distances: ", gameState.data.ghostDistances
        # Puntos de comida restantes
        print "Pac dots: ", gameState.getNumFood()
        # Distancia de manhattan a la comida mas cercada
        print "Distance nearest pac dots: ", gameState.getDistanceNearestFood()
        # Paredes del mapa
        print "Map:  \n", gameState.getWalls()
        # Puntuacion
        print "Score: ", gameState.getScore()
  
        
    def chooseAction(self, gameState):
        self.countActions = self.countActions + 1
        data=self.printLineData(gameState)
        legal=gameState.getLegalActions(0)
        self.model_name = "experiment7_c4_model"
        model=load("./models/models_practica2/BEST_MODEL.joblib")
        experiments = [["totalScore", "module", "angle", "closest_posX", "closest_posY"],
                ["totalScore", "angle", "direction", "ghost_count", "closest_posX", "closest_posY"],
                ["totalScore", "angle", "ghost_count", "G1_DIST", "G2_DIST","G3_DIST","G4_DIST"],
                ["totalScore", "POSx", "POSy", "direction","ghost_count", "closest_posX", "closest_posY"],
                ["totalScore", "module", "direction", "ghost_count"],
                ["totalScore", "angle", "direction", "wall_ahead"],
                ["angle", "direction", "wall_ahead"],
                ["totalScore", "module", "direction", "ghost_count", "G1_CLOSE", "G2_CLOSE", "G3_CLOSE", "G4_CLOSE"],
                ["direction","angle", "wall_ahead", "ghost_count", "G1_DIST", "G2_DIST","G3_DIST","G4_DIST"],
                ["angle","POSx", "POSy", "closest_posX", "closest_posY", "ghost_is_close"]]

        attr = experiments[6]
        encoded_data,decoder=change_data_2(data, attr)
        print(encoded_data)
        for i in range(len(encoded_data)):
            if encoded_data[i] == None:
                encoded_data[i] = 0

        prediction=model.predict([encoded_data])
        #action=decoder.inverse_transform(prediction)
        #action=action[0]
        """
        Prueba_2/experiment6_c8_model (decent)
        Cluster 0 -> West
        Cluster 1 -> Stop
        Cluster 2 -> East
        Cluster 3 -> South
        Cluster 4 -> South
        Cluster 5 -> East
        Cluster 6 -> West
        Cluster 7 -> North

        Prueba_3/experiment7_c4_model (BEST)
        Cluster 0 -> South
        Cluster 1 -> North
        Cluster 2 -> East
        Cluster 3 -> West

        Prueba_3/experiment7_c8_model (also good)
        Cluster 0 -> East
        Cluster 1 -> North
        Cluster 2 -> West
        Cluster 3 -> North
        Cluster 4 -> South
        Cluster 5 -> West
        Cluster 6 -> South
        Cluster 7 -> East
        """
        if prediction == 0:
            action = "South"
        if prediction == 1:
            action = "North"
        if prediction == 2:
            action = "East"
        if prediction == 3:
            action = "West"
        if prediction == 4:
            action = "South"
        if prediction == 5:
            action = "West"
        if prediction == 6:
            action = "South"
        if prediction == 7:
            action = "East"
        if prediction == 8:
            action = "Stop"
        if prediction == 9:
            action = "East"

        print("Cluster {} -> {}".format(prediction, action))

        if action not in legal or action == 'Stop':
            move_random = random.randint(0, 3)
            move=Directions.STOP
            if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
            if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
            if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
            if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        
            return move
        else:
            return action
            """
            move_random = random.randint(0, 3)
            move=Directions.STOP
            if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
            if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
            if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
            if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH"""
        


"""
class BasicAgentAA(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
    def ghost_close(self, ghost_dist):
        if True in ghost_dist: return True
        else: return False 

    def printLineData(self,gameState, last=False):
        
        #Input:
         #   gameState
        #Output:
        #    All attributes in state
        

        
       
        #Change this to the real action if you want correctly the .arff dataset
        action = self.chooseAction(gameState)


        legal = [a for a in gameState.getLegalPacmanActions()]
        if action == "Stop":
            wall_ahead = True
        else: 
            wall_ahead = False
             
        ghost_distance=gameState.data.ghostDistances
        ghost_distance=list(filter(None,ghost_distance))

        min_distance=min(ghost_distance)
        
        index=gameState.data.ghostDistances.index(min_distance)
        
        ghost_pos1=gameState.getGhostPositions()[index][0]
        ghost_pos2=gameState.getGhostPositions()[index][1]
        ghost_list = gameState.getLivingGhosts()
        vector = (ghost_pos1-gameState.getPacmanPosition()[0], ghost_pos2-gameState.getPacmanPosition()[1])
        ghost_in_action1=ghost_in_action2=ghost_in_action3=ghost_in_action4=False


        if vector[0]==-1 and (-1<=vector[1] or vector[1]<=1):
            ghost_in_action1=True
        elif vector[0]==1 and (-1<=vector[1] or vector[1]<=1):
            ghost_in_action2=True
        elif vector[1]==-1 and (-1<=vector[0] or vector[0]<=1):
            ghost_in_action3=True
        elif vector[1]==-1 and (-1<=vector[0] or vector[0]<=1):
            ghost_in_action4=True
        else:
            ghost_in_action1=ghost_in_action2=ghost_in_action3=ghost_in_action4=False

        ghost_list = [ghost_in_action1,ghost_in_action2,ghost_in_action3,ghost_in_action4]
        ghost_is_close = self.ghost_close(ghost_list)

        module = round((vector[0]**2+vector[1]**2)**0.5,2)
        epsilon = 1e-8
        angle = round(np.rad2deg(np.arctan2(vector[1],(vector[0]+epsilon))),2)
        count = ghost_list.count(True)
       
        #Datos totales recogidos: score, pacman pos, module, angle, pacman direcc, wall_ahead, ghost pos, living ghost, ghost count, ghost dist, closest ghost pos,ghost_in_action, ghost is close,  action  
        data = [gameState.getScore(),
                gameState.getPacmanPosition()[0],
                gameState.getPacmanPosition()[1],
                module,
                angle,
                gameState.data.agentStates[0].getDirection(),
                wall_ahead, 
                gameState.getGhostPositions()[0][0], 
                gameState.getGhostPositions()[0][1],
                gameState.getGhostPositions()[1][0],
                gameState.getGhostPositions()[1][1],
                gameState.getGhostPositions()[2][0], 
                gameState.getGhostPositions()[2][1],
                gameState.getGhostPositions()[3][0], 
                gameState.getGhostPositions()[3][1], 
                gameState.getLivingGhosts()[1], 
                gameState.getLivingGhosts()[2], 
                gameState.getLivingGhosts()[3], 
                gameState.getLivingGhosts()[4],
                count, 
                gameState.data.ghostDistances[0],
                gameState.data.ghostDistances[1],
                gameState.data.ghostDistances[2],
                gameState.data.ghostDistances[3],
                ghost_pos1,ghost_pos2,ghost_in_action1,ghost_in_action2,ghost_in_action3,ghost_in_action4,ghost_is_close,action]
        #Change last line to complete the circuit
        if last == True:
            data[1] = ghost_pos1
            data[2] = ghost_pos2
            data[3]=0.0
            data[15]=data[16]=data[17]=data[18] = False
            data[19]=data[20]=data[21]=data[22]=data[23]=data[24]=data[25] = 0
            data[-2]=data[-3]=data[-4]=data[-5]=data[-6]=False
            data[-1] = "Stop"


        return data

    def printInfo(self, gameState):
        print "---------------- TICK ", self.countActions, " --------------------------"
        # Dimensiones del mapa
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print "Width: ", width, " Height: ", height
        # Posicion del Pacman
        print "Pacman position: ", gameState.getPacmanPosition()
        # Acciones legales de pacman en la posicion actual
        print "Legal actions: ", gameState.getLegalPacmanActions()
        # Direccion de pacman
        print "Pacman direction: ", gameState.data.agentStates[0].getDirection()
        # Numero de fantasmas
        print "Number of ghosts: ", gameState.getNumAgents() - 1
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        print "Living ghosts: ", gameState.getLivingGhosts()
        # Posicion de los fantasmas
        print "Ghosts positions: ", gameState.getGhostPositions()
        # Direciones de los fantasmas
        print "Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Distancia de manhattan a los fantasmas
        print "Ghosts distances: ", gameState.data.ghostDistances
        # Puntos de comida restantes
        print "Pac dots: ", gameState.getNumFood()
        # Distancia de manhattan a la comida mas cercada
        print "Distance nearest pac dots: ", gameState.getDistanceNearestFood()
        # Paredes del mapa
        print "Map:  \n", gameState.getWalls()
        # Puntuacion
        print "Score: ", gameState.getScore()
        #Linea de datos
        #print "LineData: ", self.printLineData(gameState)
        
        
    def chooseAction(self, gameState):
        self.countActions = self.countActions + 1
        self.printInfo(gameState)
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        #ghost=gameState.getLivingGhosts()
        ghost_distance=gameState.data.ghostDistances
        ghost_distance=list(filter(None,ghost_distance))
        print("GHOST DISTANCE",ghost_distance)
        min_distance=min(ghost_distance)
        index=gameState.data.ghostDistances.index(min_distance)
        print(index)
        ghost_pos=gameState.getGhostPositions()[index]
        pacman_pos=gameState.getPacmanPosition()

        tupla=[ghost_pos[0]-pacman_pos[0],ghost_pos[1]-pacman_pos[1]]
        print(tupla)
        tupla_absoluta=[abs(ele) for ele in tupla]
        if 0 in tupla_absoluta:
            aux=tupla_absoluta.index(0)
            if aux==0:
                index_escoger_direccion=1
            else:
                index_escoger_direccion=0
        else:
            index_escoger_direccion=min(tupla_absoluta)
        if index_escoger_direccion==0:
            if (tupla[0]>0) and Directions.EAST in legal:
                move=Directions.EAST
                segunda_eleccion=False
            elif (tupla[0]>0) and Directions.EAST not in legal:
                segunda_eleccion=True
                index_escoger_direccion=1

            elif (tupla[0]<0) and Directions.WEST in legal:
                move = Directions.WEST
                segunda_eleccion=False
            elif (tupla[0]<0) and Directions.WEST not in legal:
                segunda_eleccion=True
                index_escoger_direccion=1
            else:
                if Directions.NORTH in legal:
                    move=Directions.NORTH
                elif Directions.SOUTH in legal:
                    move = Directions.SOUTH

        else:
            if (tupla[1]>0) and Directions.NORTH in legal:
                move = Directions.NORTH
                segunda_eleccion=False
            elif (tupla[1]>0) and Directions.NORTH not in legal:
                segunda_eleccion=True
                index_escoger_direccion=0

            elif (tupla[1]<0) and Directions.SOUTH in legal:
                move = Directions.SOUTH
                segunda_eleccion=False
            elif (tupla[1]<0) and Directions.SOUTH not in legal:
                segunda_eleccion=True
                index_escoger_direccion=0
            else:
                if Directions.EAST in legal:
                    move=Directions.EAST
                elif Directions.WEST in legal:
                    move = Directions.WEST
        randomizar=False
        
        if segunda_eleccion:
            if index_escoger_direccion==0:
                if (tupla[0]>0) and Directions.EAST in legal:
                    move=Directions.EAST
                    randomizar=False
                elif (tupla[0]>0) and Directions.EAST not in legal:
                    randomizar=True
                    index_escoger_direccion=1

                elif (tupla[0]<0) and Directions.WEST in legal:
                    move = Directions.WEST
                    randomizar=False
                elif (tupla[0]<0) and Directions.WEST not in legal:
                    randomizar=True
                    index_escoger_direccion=1
                elif randomizar==False:
                    randomizar=True

            else:
                if (tupla[1]>0) and Directions.NORTH in legal:
                    move = Directions.NORTH
                    randomizar=False
                elif (tupla[1]>0) and Directions.NORTH not in legal:
                    randomizar=True
                    index_escoger_direccion=0

                elif (tupla[1]<0) and Directions.SOUTH in legal:
                    move = Directions.SOUTH
                    randomizar=False
                elif (tupla[1]<0) and Directions.SOUTH not in legal:
                    randomizar=True
                    index_escoger_direccion=0
                elif randomizar==False:
                    randomizar=True

        else:
            randomizar=False
        print("randomizar",randomizar)
        if randomizar:
            move_random = random.randint(0, 3)
            if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
            if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
            if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
            if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        
        return move
"""