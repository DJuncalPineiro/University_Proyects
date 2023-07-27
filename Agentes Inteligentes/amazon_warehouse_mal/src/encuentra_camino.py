#!/usr/bin/env python
#from types import NoneType
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
    def __init__(self,mapa,padre,tipo):
        self.mapa=mapa
        self.padre=padre
        self.tipo=tipo
        """
        tipo:
            -'move':coste=1
            -'turn_right': coste=2
            -'turn_left': coste=2
    
            -'move_pallet': coste=
        """
        if np.argwhere(mapa==100).any():
            self.goal_pose = np.argwhere(mapa==100)[0]
        else:
            self.goal_pose = np.array([0,0])
        if np.argwhere(mapa==1).any():
            self.posicion=np.argwhere(mapa==1)[0]
        else:
            self.posicion = self.goal_pose#posicinoes en la matriz
        self.g = self.coste_transcurrido()
        self.f=self.coste_total()
        self.orientacion=self.orienta()
        #print("tipooo",self.tipo)
    
    def __str__(self):
        str = ""
        for i in range(len(self.mapa)):
            str = str +"{}\n".format(self.mapa[i])
        str = str + "{}\n".format(self.tipo)
        str= str + "{}\n".format(self.orientacion)
        #str=str+"padre{}\n".format(self.padre)
        return str
    
    def orienta(self):
        if self.padre:
            if 'right' in self.tipo:
                #print("**********************************************")
                self.orientacion=(self.padre.orientacion)
                #print("orienta_padre",self.orientacion)
                self.orientacion=self.orientacion-90
                #print("orienta",self.orientacion)
                if self.orientacion>=360:
                    self.orientacion=self.orientacion-360
                if self.orientacion<0:
                    self.orientacion=self.orientacion+360
                #print("orienta_final",self.orientacion)
            if 'left' in self.tipo:
                #print("------------------------------------")
                #print("orienta_padre",self.padre.orientacion)
                self.orientacion=(self.padre.orientacion+90)
                if self.orientacion>=360:
                    self.orientacion=self.orientacion-360
                if self.orientacion<0:
                    self.orientacion=self.orientacion+360
                #print("orienta_final",self.orientacion)

            if 'move' in self.tipo:
                self.orientacion=self.padre.orientacion
        if not self.padre:
            self.orientacion=0
        return self.orientacion
        
        #f
    def coste_total(self):
        #g=self.coste_transcurrido()
        h=self.coste_estimado()
        #print("f",np.abs(self.g+h))
        return self.g+h
    
    #g
    def coste_transcurrido(self):
        if self.padre:
            coste=self.padre.g
            if 'pallet' not in self.tipo:
                if 'move' in self.tipo:
                    coste+=1
                if 'turn' in self.tipo:
                    coste+=3
            else:
                if 'move' in self.tipo:
                    coste+=2
                if 'turn' in self.tipo:
                    coste+=4
        if not self.padre:
            coste=0
            """
            if 'move' in self.tipo:
                self.g+=1
            if 'turn' in self.tipo:
                self.g+=2
            """   
        #print("g",coste) 
        return coste
    #h
    def coste_estimado(self):
        if self.padre:
            x=self.goal_pose[0]-self.posicion[0]
            y=self.goal_pose[1]-self.posicion[1]
            if x==0 or y==0:
                #print("**************************************************************************************************************")
                return 0
            else:
            #print("h",x**2+y**2)
                #print('H',x**2+y**2)
                return np.sqrt(x**2+y**2)
        if not self.padre:
            return 0
        #return 0
    
    
    
    

    
class Busqueda_estrella:
    def __init__(self,final=100,map=0):
        self.mapa=map
        self.nav=navigation.Navigation()
        #orientacion: 1:palante, 2:dcha, 3:izq, 4:atras
        self.nodo_inicial = Estado(self.mapa, None, None)
        self.final=final
        if np.argwhere(self.mapa==self.final).any():
            self.goal_pose = np.argwhere(self.mapa==self.final)[0]
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
            self.goal_pose = np.array([0,0])        
        self.exito = False
        self.lista_cerrada=[]
        self.lista_abierta=[self.nodo_inicial]
        self.Estrella()

    
    
    
    
    def expandir_nodo(self,current_nodo):
        mapa_1=current_nodo.mapa.copy()
        mapa_2=current_nodo.mapa.copy()
        mapa_3=current_nodo.mapa.copy()
        hijo_turn_right=None
        hijo_turn_left=None
        hijo_move=None
        lista_ordenar=[]
        
        if current_nodo.orientacion==0:
            #print("1")
            if mapa_1[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==0 or mapa_1[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==100: #si la casilla esta vacia
                mapa_1[current_nodo.posicion[0]-1][current_nodo.posicion[1]]=1 #colocamos un uno
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]]=current_nodo.f
                hijo_move=Estado(mapa_1,current_nodo,'move')
                lista_ordenar.append(hijo_move)

            if mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==0 or mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==100:
                mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==1
                mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]]==current_nodo.f
                hijo_turn_right=Estado(mapa_2,current_nodo,'turn_right')
                lista_ordenar.append(hijo_turn_right)
                
            if mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==0 or mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==100:
                mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==1
                mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]]==current_nodo.f
                hijo_turn_left=Estado(mapa_3,current_nodo,'turn_left')
                lista_ordenar.append(hijo_turn_left)

        elif current_nodo.orientacion==270:
            #print("2")
            if mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==0 or mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==100:
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]+1]=1
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]]=current_nodo.f
                hijo_move=Estado(mapa_1,current_nodo,'move')
                lista_ordenar.append(hijo_move)
                
    
            if mapa_2[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==0 or mapa_2[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==100:
                mapa_2[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==1
                mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]]==current_nodo.f
                hijo_turn_right=Estado(mapa_2,current_nodo,'turn_right')
                lista_ordenar.append(hijo_turn_right)
    
            if mapa_3[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==0 or mapa_3[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==100:
                mapa_3[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==1
                mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]]==current_nodo.f
                hijo_turn_left=Estado(mapa_3,current_nodo,'turn_left')
                lista_ordenar.append(hijo_turn_left)

    
        elif current_nodo.orientacion==90:
            #print("3")
            if mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==0 or mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==100:
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]-1]=1
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]]=current_nodo.f
                hijo_move=Estado(mapa_1,current_nodo,'move')
                lista_ordenar.append(hijo_move)
                
    
            if mapa_2[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==0 or mapa_2[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==100:
                mapa_2[current_nodo.posicion[0]-1][current_nodo.posicion[1]]==1
                mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]]==current_nodo.f
                hijo_turn_right=Estado(mapa_2,current_nodo,'turn_right')
                lista_ordenar.append(hijo_turn_right)
    
            if mapa_3[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==0 or mapa_3[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==100:
                mapa_3[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==1
                mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]]==current_nodo.f
                hijo_turn_left=Estado(mapa_3,current_nodo,'turn_left')
                lista_ordenar.append(hijo_turn_left)

        elif current_nodo.orientacion==180:
            #print("4")
            if mapa_1[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==0 or mapa_1[current_nodo.posicion[0]+1][current_nodo.posicion[1]]==100:
                mapa_1[current_nodo.posicion[0]+1][current_nodo.posicion[1]]=1
                mapa_1[current_nodo.posicion[0]][current_nodo.posicion[1]]=current_nodo.f
                hijo_move=Estado(mapa_1,current_nodo,'move')
                lista_ordenar.append(hijo_move)
                
            if mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==0 or mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==100:
                mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]-1]==1
                mapa_2[current_nodo.posicion[0]][current_nodo.posicion[1]]==current_nodo.f
                hijo_turn_right=Estado(mapa_2,current_nodo,'turn_right')
                lista_ordenar.append(hijo_turn_right)

            if mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==0 or mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==100:
                mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]+1]==1
                mapa_3[current_nodo.posicion[0]][current_nodo.posicion[1]]==current_nodo.f
                hijo_turn_left=Estado(mapa_3,current_nodo,'turn_left')
                lista_ordenar.append(hijo_turn_left)
        

        lista_ordenada=self.reordenar_nodos(lista_ordenar)
        #print("len",len(lista_ordenada))
        for i in range(len(lista_ordenada)):
            #print("lista_ordenada",lista_ordenada[i].tipo)
            
            self.lista_abierta.append(lista_ordenada[i])
        #print("---")

        #print(self.lista_abierta)
        
            
    def reordenar_nodos(self, nodes): 
        nodes_f = []
        ordenada=[]
        for i in range(len(nodes)): #metemos las f de los nodos en una lista nodes_f
            nodes_f.append(nodes[i].f)
            ordenada.append(nodes[i])
        
        nodes_f.sort()

        
        #print("nodes_f_ordenada",nodes_f)
        i=0
        while nodes:
            #print("len",len(nodes))
            #print("index",nodes_f.index(nodes[i].f))
            if nodes_f.index(nodes[i].f)==0:
                ordenada[0]=(nodes[i])
                #print("0",ordenada[0].tipo)
                nodes.pop(i)
                if len(nodes)<1:
                    break
                #print("len",len(nodes))

                
                
            if nodes_f.index(nodes[i].f)==1:
                ordenada[1]=nodes[i]
                #print("1",ordenada[1].tipo)
                nodes.pop(i)
                if len(nodes)<1:
                    break
                #print("len",len(nodes))

                

            if nodes_f.index(nodes[i].f)==2:
                ordenada[2]=nodes[i]
                #print("2",ordenada[2].tipo)
                nodes.pop(i)
                if len(nodes)<1:
                    break
            else:
                break
                

        
        #print(ordenada)
        """
        for i in range(3):
            self.lista_abierta.append(nodes[i])
        """
        return ordenada
        
        


    
    def Estrella(self):
        suma=0
        while not self.exito:
            #if self.lista_abierta[0] not in self.lista_cerrada:
            if not self.evaluar():
                if len(self.lista_abierta)<1:
                    self.exito=True
                    running=True
                    print("LEN POCO")
                    break
                #print(self.lista_abierta[0].posicion,self.goal_pose)
                #print((self.lista_abierta[0].posicion==self.goal_pose).all())
                #print("1",len(self.lista_abierta))
                
                if (self.lista_abierta[0].posicion==self.goal_pose).all():
                    self.lista_cerrada.append(self.lista_abierta[0])
                    nodito = self.lista_cerrada[-1]
                    print(nodito)
                    self.exito=True
                    running=True
                    break
                else:

                    self.lista_cerrada.append(self.lista_abierta[0])
                    self.expandir_nodo(self.lista_cerrada[-1])
                    nodito = self.lista_cerrada[-1]
                    #print(nodito)
                    self.lista_abierta.pop(0)
                
            else:
                #print("hola")
                #print("2",len(self.lista_abierta))
                
            
                if len(self.lista_abierta)<1:
                #if (self.lista_abierta[0].posicion==self.goal_pose).all():
                    print("LEN POCO_1")
                    self.exito=True
                    running=True
                    break
                if (self.lista_abierta[0].posicion==self.goal_pose).all():
                    print("LEN POCO_2")
                    self.exito=True
                    running=True
                    break
                self.lista_abierta.pop(0)
            suma+=1
        print("Bucle",suma)
            
        
        print("Enhorabuena, se ha conseguido una solucion")
        ruta=[]
        coste_total=(self.lista_cerrada[-1]).f
        while running:
            nodo_actual=self.lista_cerrada[-1]
            while nodo_actual:
                tupla=[nodo_actual.tipo,1]
                ruta.append(tupla)
                nodo_actual=nodo_actual.padre
            running=False
        print("Coste total",coste_total)
        
        ruta=ruta[::-1]
        print("ruta",ruta)
        i=0
        while i<len(ruta):
            try:
                suma=ruta[i][1]
                if ruta[i][0]==ruta[i+1][0]:
                    #print("Repetido",ruta[i][0])
                    #print("suma",suma+1)
                    #print("i",i)
                    suma+=1
                    ruta[i+1][1]=suma
                    ruta.pop(i)
                
                else:
                    i+=1
                    pass
            except:
                break
        for i in range(len(ruta)):
            if ruta[i][1]==3 and ruta[i][0]=='turn_left':
                #print('AAAAAAAAAAAAAA')
                ruta[i][0]='turn_right'
                ruta[i][1]=1
            if ruta[i][1]==3 and ruta[i][0]=='turn_right':
                #print('BBBBBBBBB')
                ruta[i][0]='turn_left'
                ruta[i][1]=1
        print("Ruta final",ruta)
        comandos=self.trace_route(ruta)

                
    def evaluar(self):
        evaluacion=False
        if len(self.lista_cerrada)>0 and len(self.lista_abierta)>0:
            for i in range(len(self.lista_cerrada)):
                if (self.lista_abierta[0].mapa==self.lista_cerrada[i].mapa).all() and (self.lista_abierta[0].orientacion==self.lista_cerrada[i].orientacion) and (self.lista_abierta[0].tipo==self.lista_cerrada[i].tipo) and (self.lista_abierta[0].posicion==self.lista_cerrada[i].posicion).all() and (self.lista_abierta[0].padre==self.lista_cerrada[i].padre):
                    #print("Abierta",self.lista_abierta[0].mapa)
                    #print("cerrada",self.lista_cerrada[i].mapa)
                    evaluacion=True
        
        #print(evaluacion)
        return evaluacion
    

    def trace_route(self,ruta):
        
        for move, n in ruta:
            if move == 'move':
                self.nav.move(n)
            elif move == 'turn_right':
                for i in range(n):
                    self.nav.rotateRight()
                    #self.nav.move(1)
            elif move == 'turn_left':
                for i in range(n):
                    self.nav.rotateLeft()
                    #self.nav.move(1)
            else:
                pass
    
    
mapa_1=np.array([[9,9,9,9,9,9,9,9],
                 [9,0,0,0,0,0,0,9],
                 [9,0,0,0,0,0,0,9],
                 [9,9,9,9,0,0,0,9],
                 [9,0,0,0,0,0,0,9],
                 [9,0,100,0,0,0,0,9],
                 [9,0,0,0,9,9,9,9],
                 [9,0,9,0,0,0,0,9],
                 [9,0,9,0,1,0,0,9],
                 [9,9,9,9,9,9,9,9]])
mapa_2=np.array([[9,9,9,9,9,9,9,9],
                 [9,0,0,0,0,100,0,9],
                 [9,0,0,0,0,0,0,9],
                 [9,9,9,9,0,0,0,9],
                 [9,0,0,0,0,0,0,9],
                 [9,0,1,0,0,0,0,9],
                 [9,0,0,0,9,9,9,9],
                 [9,0,0,0,0,0,0,9],
                 [9,0,0,0,0,0,0,9],
                 [9,9,9,9,9,9,9,9]])
pallet=Busqueda_estrella(100,mapa_1)
posicion_final=Busqueda_estrella(100,mapa_2)

  