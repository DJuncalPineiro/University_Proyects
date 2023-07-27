#!/usr/bin/env python
from types import NoneType
from numpy.core.numeric import Inf
import rospy
from utils import navigation
import numpy as np
#Estados con su coste
move_forward=1
turn=2
uplift=3
downlift=3
pallet=False
if pallet:
    move=2
    turn=3

 

 
class Estado:
    def __init__(self,mapa,tipo):
        self.mapa=mapa
        self.padre=None
        self.tipo=tipo
        """
        tipo:
            -'move':coste=1
            -'turn_right': coste=2
            -'turn_left': coste=2
    
            -'move_pallet': coste=
        """
        if np.argwhere(mapa==2).any():
            self.goal_pose = np.argwhere(mapa==2)[0]
        else:
            self.goal_pose = np.array([0,0])
        self.posicion = np.argwhere(mapa==1)[0]#posicinoes en la matriz
        self.g = 0
        self.h = 0
        self.orientacion=0

    def __str__(self):
        str = ""
        for i in range(len(self.mapa)):
            str = str +"{}\n".format(self.mapa[i])
        str = str + "{}\norienta {}\n".format(self.tipo, self.orientacion)
        return str
    

    def orienta(self):
        if self.padre:
            self.orientacion = self.padre.orientacion
            if 'turn_right' in self.tipo:
                self.orientacion=(self.padre.orientacion-90)
                if self.orientacion>=360:
                    self.orientacion=self.orientacion-360
                if self.orientacion<360:
                    self.orientacion=self.orientacion+360
            if 'turn_left' in self.tipo:
                self.orientacion=(self.padre.orientacion+90)
                if self.orientacion>=360:
                    self.orientacion=self.orientacion-360
                if self.orientacion<0:
                    self.orientacion=self.orientacion+360
            else:
                self.orientacion=self.padre.orientacion
        else:
            return 0
        
        return self.orientacion
        
        #f
    def coste_total(self):
        return self.g+self.h
    
    #g
    def G(self):
        if self.padre:   
            coste = 0
            if 'pallet' not in self.tipo:
                if 'move' in self.tipo:
                    coste+= 1
                if 'turn' in self.tipo:
                    coste += 2
            else:
                if 'move' in self.tipo:
                    coste+= 2
                if 'turn' in self.tipo:
                    coste += 3
                return coste
        else:
            return 0
    
    def coste_movimiento(self):
        if self.tipo:
            if 'pallet' not in self.tipo:
                if 'move' in self.tipo:
                    return 1
                if 'turn' in self.tipo:
                    return 2
            else:
                if 'move' in self.tipo:
                    return 2
                if 'turn' in self.tipo:
                    return 3
        else: 
            return 0
            """
                if 'move' in self.tipo:
                    self.g+=1
                if 'turn' in self.tipo:
                    self.g+=2
                """    
    #h
    def H(self):
        x=self.goal_pose[0]-self.posicion[0]
        y=self.goal_pose[1]-self.posicion[1]
        h = abs(x+y)
        return h+2

        #return h
    
    
    
    
    
    
class Busqueda_estrella:
    def __init__(self):
        self.mapa=np.array([[9,9,9,9,9,9,9,9,9,9],
                    [9,0,0,0,0,0,0,0,0,9],
                    [9,0,0,0,0,0,0,0,0,9],
                    [9,0,2,0,0,0,0,0,0,9],
                    [9,0,0,0,0,0,0,0,0,9],
                    [9,0,0,0,0,0,0,0,0,9],
                    [9,0,0,0,0,0,0,0,0,9],
                    [9,0,0,0,0,0,0,1,0,9],
                    [9,0,0,0,0,0,0,0,0,9],
                    [9,9,9,9,9,9,9,9,9,9]])

        #orientacion: 1:palante, 2:dcha, 3:izq, 4:atras
        self.nodo_inicial = Estado(self.mapa, None)
        print("nodo inicial", self.nodo_inicial)
        if np.argwhere(self.mapa==2).any():
            self.goal_pose = np.argwhere(self.mapa==2)[0]
        else:
            self.goal_pose = np.array([0,0])     
        self.exito = False
        self.Estrella()
    
    
    
    
    def expandir_nodo(self,current_nodo):
        mapa_1=current_nodo.mapa.copy()
        mapa_2=current_nodo.mapa.copy()
        mapa_3=current_nodo.mapa.copy()
        hijo_turn_right=None
        hijo_turn_left=None
        hijo_move=None
        current_nodo.orienta()
        if current_nodo.orientacion==0:
            if mapa_1[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==0 or mapa_1[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==2: #si la casilla esta vacia
                mapa_1[current_nodo.posicion[0]-1][current_nodo.posicion[1]]=1 #colocamos un uno
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]]=current_nodo.g + current_nodo.h
                hijo_move=Estado(mapa_1,'move')
            elif mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==0 or mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]+1] ==2:                
                hijo_turn_right=Estado(mapa_2,'turn_right')
            elif mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==0 or mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==2:
                
                hijo_turn_left=Estado(mapa_3,'turn_left')

        if current_nodo.orientacion==-90:
            print("2")
            if mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==0 or mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==2:
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]+1]=1
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]]=current_nodo.g + current_nodo.h
                hijo_move=Estado(mapa_1,'move')
    
            elif mapa_2[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==0 or mapa_2[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==2:
                
                hijo_turn_right=Estado(mapa_2,'turn_right')
    
            elif mapa_3[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==0 or mapa_3[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==2:
                
                hijo_turn_left=Estado(mapa_3,'turn_left')
    
        if current_nodo.orientacion==90:
            if mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==0 or mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==2:
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]-1]=1
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]]=current_nodo.g + current_nodo.h
                hijo_move=Estado(mapa_1,'move')
    
            if mapa_2[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==0 or mapa_2[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==2:
                
                hijo_turn_right=Estado(mapa_2,'turn_right')
    
            if mapa_3[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==0 or mapa_3[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==2:
                
                hijo_turn_left=Estado(mapa_3,'turn_left')
        if current_nodo.orientacion==180:
            print("4")
            if mapa_1[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==0 or mapa_1[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==2:
                mapa_1[current_nodo.posicion[0]+1][current_nodo.posicion[1]]=1
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]]=current_nodo.g + current_nodo.h
                hijo_move=Estado(mapa_1,'move')
            if mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==0 or mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==2:
                
                hijo_turn_right=Estado(mapa_2,'turn_right')
            if mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==0 or mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==2:
    
                hijo_turn_left=Estado(mapa_3,'turn_left')
        
        nodos_expandidos = [hijo_move, hijo_turn_right, hijo_turn_left]
        
        for nodo in nodos_expandidos:
            if type(nodo) == NoneType:
                nodos_expandidos.remove(nodo)
            print(nodo)
        return nodos_expandidos

    def Estrella(self):
        openset = set()
        closedset = set()
        #Current point is the starting point
          
        #Add the starting point to the open set
        openset.add(self.nodo_inicial)
        #While the open set is not empty
        while openset and not self.exito:
            #Find the item in the open set with the lowest G + H score
            current = min(openset, key=lambda i:i.g+ i.h)
            print(current)
            print()
            print("(G,H) = ({},{})".format(current.g, current.h))
            print(self.goal_pose)
            print("orienta", current.orientacion)
            #If it is the item we want, retrace the ruta and return it
            if (current.posicion == self.goal_pose).all():
                self.exito = True
                ruta = []
                while current.padre:
                    ruta.append(current.tipo)
                    current = current.padre
                ruta.append(current.tipo)
                print(ruta[::-1]) #le damos la vuelta a la secuencia de movimientos
            #Remove the item from the open set
            openset.remove(current)
            #Add it to the closed set
            closedset.add(current)
            #Loop through the node's children/siblings
            for node in self.expandir_nodo(current):
                #If it is already in the closed set, skip it
                if node in closedset:
                    continue
                #Otherwise if it is already in the open set
                if node in openset:
                    #Check if we beat the G score 
                    new_g = current.g + current.coste_movimiento()
                    if node.g > new_g:
                        #If so, update the node to have a new parent
                        node.g = new_g
                        node.padre = current
                else:
                    #If it isn't in the open set, calculate the G and H score for the node
                    node.g = current.g + current.coste_movimiento()
                    node.h = current.H()
                    #Set the parent to our current item
                    node.padre = current
                    node.orienta()
                    #Add it to the set
                    print("node", node)
                    openset.add(node)
        raise ValueError('No se ha encontrado camino')
main = Busqueda_estrella()
    
"""     
    if hijo_move and hijo_turn_left and hijo_turn_right:
    
            if hijo_move.f<hijo_turn_right.f:
                if hijo_turn_right.f<hijo_turn_left.f:
                    self.lista_abierta.append(hijo_turn_left)
                    self.lista_abierta.append(hijo_turn_right)
                    self.lista_abierta.append(hijo_move)
    
                if hijo_move.f<hijo_turn_left.f:
                    self.lista_abierta.append(hijo_turn_right)
                    #print("abierta",self.lista_abierta)
    
                    self.lista_abierta.append(hijo_turn_left)
                    self.lista_abierta.append(hijo_move)
                else:
                    self.lista_abierta.append(hijo_turn_right)
                    self.lista_abierta.append(hijo_move)
                    self.lista_abierta.append(hijo_turn_left)
            else:
                if hijo_move.f<hijo_turn_left.f:
                    self.lista_abierta.append(hijo_turn_left)
                    self.lista_abierta.append(hijo_move)
                    self.lista_abierta.append(hijo_turn_right)
                if hijo_turn_right.f<hijo_turn_left.f:
                    self.lista_abierta.append(hijo_move)
                    self.lista_abierta.append(hijo_turn_left)
                    self.lista_abierta.append(hijo_turn_right)
                else:
                    self.lista_abierta.append(hijo_move)
                    self.lista_abierta.append(hijo_turn_right)
                    self.lista_abierta.append(hijo_turn_left)    
        if not hijo_move and hijo_turn_left and hijo_turn_right:
            if hijo_turn_left.f<hijo_turn_right.f:
                self.lista_abierta.append(hijo_turn_right)
                self.lista_abierta.append(hijo_turn_left)
            else:
                self.lista_abierta.append(hijo_turn_left)
                self.lista_abierta.append(hijo_turn_right)
        if not hijo_turn_right and hijo_move and hijo_turn_left:
            if hijo_move.f<hijo_turn_left.f:
                self.lista_abierta.append(hijo_turn_left)
                self.lista_abierta.append(hijo_move)
            else:
                self.lista_abierta.append(hijo_move)
                self.lista_abierta.append(hijo_turn_left)  
        if not hijo_turn_left and hijo_turn_right and hijo_move:           
            if hijo_move.f<hijo_turn_right.f:
                self.lista_abierta.append(hijo_turn_right)
                self.lista_abierta.append(hijo_move)   
            else:
                self.lista_abierta.append(hijo_move)
                self.lista_abierta.append(hijo_turn_right)      
    
    
        if not hijo_move and not hijo_turn_right and hijo_turn_left:
            self.lista_abierta.append(hijo_turn_left)
        if not hijo_turn_left and not hijo_turn_right and hijo_move:
            self.lista_abierta.append(hijo_move)
        if not hijo_move and not hijo_turn_left and hijo_turn_right:
            self.lista_abierta.append(hijo_turn_right)"""
            
        
"""            
    def reordenar_nodos(self, nodes): 
        nodes_f = []
        for i in range(len(nodes)): #metemos las f de los nodos en una lista nodes_f
            if type(nodes[i]) != NoneType:
                nodes_f.append(nodes[i].f)
            else:
                nodes_f.append(1000) #como es una lista auxiliar
        for j in range(2):
            for i in range(2): 
                if nodes_f[i+1] < nodes_f[i]: #segun la f, reordena la lista nodos 
                    nodes[i],nodes[i+1] =  nodes[i+1],nodes[i]
                    nodes_f[i],nodes_f[i+1] =  nodes_f[i+1],nodes_f[i]
        print(nodes_f)
        for i  in range(len(nodes)):
            if type(nodes[i]) == NoneType:
                nodes.pop(i)
            
        return nodes"""

   
"""def Estrella(self):
        while not self.exito:
            if self.lista_abierta[0] in self.lista_cerrada:
                cmp = (self.lista_abierta[0].posicion==self.goal_pose).all()
                if cmp:
                    self.exito=True
                    running=True
                else:
                    self.lista_cerrada.append(self.lista_abierta[0])
                    S = self.expandir_nodo(self.lista_cerrada[-1])
                    for s in S:
                        self.lista_abierta.append(s)
                    nodito = self.lista_abierta[0]
                    print(nodito)                        
            else:
                self.lista_abierta.pop(0)
    
        def Estrella(self):
        while not self.exito:
            N = self.lista_abierta.pop(0)
            cmp = (N.posicion==self.goal_pose).all()
            if cmp:
                self.exito=True
                running=True
            else:
                self.lista_cerrada.append(N)
                S = self.expandir_nodo(N)
                for s in S:
                    if s in self.lista_cerrada:
                        pass
                    elif (s not in self.lista_abierta) and (s not in self.lista_cerrada):
                        self.lista_abierta.append(s)
                        
                print(N)                        
        else:
            self.lista_abierta.pop(0)
            """

    
"""print("Enhorabuena, se ha conseguido una solucion")
    ruta=[]
    coste_total=(self.lista_cerrada[-1]).f
    while running:
        nodo_actual=self.lista_cerrada[-1]
        while nodo_actual.padre:
            ruta.append(nodo_actual.tipo)
            nodo_actual=nodo_actual.padre
        running=False
    print("Ruta final",ruta[:-1])
    print("Coste total",coste_total)"""
    
                
    
    
    
    
    

"""
    def obs():
        global obstacles_pos
        obstacles_pos=[] #Aadir los obstaculos como una tupla (posx,posy)
        #len(obstacles_pos)==n #obstaculos que tenemos
    def pallet_pos():
        global pallet_pos
        pallet_pos=[]#tupla de (posx,posy)



    def g(nodo):
        actual=nodo
        self.g=0
        while actual!=nodo_inicial:
            self.g=self.g+actual
            actual=nodo.padre()
        return self.g


    def h(nodo):
        nodo_actual=nodo
        busqueda(nodo_actual,nodo_final)




    def evaluacion(actual_state,orientacion):
        for i in range(pallet_pos):
            dist_x=pallet_pos[i][0]-pos_x
            dist_y=pallet_pos[i][1]-pos_y
            if dist_x>0 and dist_y>0 and orientacion==0 or):
                if dist_x>dist_y:
                    estado.append(go_forward(int(dist_x)))
                elif dist_x<dist_y:
                    estado.append(turn_right)
            elif dist_x>0 and dist_y>0 and orientacion==1:
                if dist_x>dist_y:
                    estado.append(turn_right)
                elif dist_x<dist_y:
                    estado.append(go_forward(int(dist_x)))
            
                
        
        
        
        
        
        
        
            for i in range(len(obstacles_pos)):
                if (pos_x==obstacles_pos[i][0]+1) and (pos_y==obstacles_pos[i][1]+ 1)   and orientacion==0 or):
                    estado.append(turn_right)
                elif (pos_x==obstacles_pos[i][0]+1) and (pos_y==obstacles_pos[i][1]+ 1)   and orientacion==1:
                    estado.append(turn_left)
                elif (pos_x==obstacles_pos[i][0]+1) and (pos_y==obstacles_pos[i][1]+ 1)   and orientacion==2:
                    estado.append(go_forward(1))
                elif (pos_x==obstacles_pos[i][0]+1) and (pos_y==obstacles_pos[i][1]+ 1)   and orientacion==3:
                    estado.append(go_forward(1))
            


        

                
    """




    #def busqueda(lista_obs,lista_pallet,init_pos,goal_pos):
        




