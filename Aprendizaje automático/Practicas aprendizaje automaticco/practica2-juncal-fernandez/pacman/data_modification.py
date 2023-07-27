from attr import attributes
from sklearn.preprocessing import LabelEncoder

#  CHANGE DATA APPLICATE TO
#   TOTALSCORE  ANGLE   DIRECTON    WALL_AHEAD      
def change_data_2(data,atributos):
    """
    input: data array with especific attributes.
    Customize:
        Change attributes in encoded_data refered to the input. In case the labelEncoder is changed, write your own encoder.
    """
    """[gameState.getScore(),0
        gameState.getPacmanPosition()[0],1
        gameState.getPacmanPosition()[1],2
        module,3
        angle,4
        gameState.data.agentStates[0].getDirection(),5
        wall_ahead, 6
        gameState.getGhostPositions()[0][0], 7
        gameState.getGhostPositions()[0][1],8
        gameState.getGhostPositions()[1][0],9
        gameState.getGhostPositions()[1][1],10
        gameState.getGhostPositions()[2][0],11 
        gameState.getGhostPositions()[2][1],12
        gameState.getGhostPositions()[3][0], 13
        gameState.getGhostPositions()[3][1], 14
        gameState.getLivingGhosts()[1], 15
        gameState.getLivingGhosts()[2], 16
        gameState.getLivingGhosts()[3], 17
        gameState.getLivingGhosts()[4],18
        count, 19
        gameState.data.ghostDistances[0],20
        gameState.data.ghostDistances[1],21
        gameState.data.ghostDistances[2],22
        gameState.data.ghostDistances[3],23
        ghost_pos1,ghost_pos2,ghost_in_action1,ghost_in_action2,ghost_in_action3,ghost_in_action4,ghost_is_close,action]"""
    #encoded_data=[data[0],data[4],data[5],data[6]]
    encoded_data=[]
    #print("case",case)
    encoder_action=LabelEncoder()
    encoder_action.fit(['Stop','East','West','North','South'])
    encoder_bool=LabelEncoder()
    encoder_bool.fit([True,False])

    labels_encoded=list(encoder_action.classes_)
    #for i,clave in enumerate(labels_encoded):
    #    print("Original->",clave,"   encoded->",i)
    
    for i in range(len(data)):
        if type(data[i]) == str:
            encoded_data.append(encoder_action.transform([data[i]]))
        elif type(data[i]) == bool:
            encoded_data.append(encoder_bool.transform([data[i]]))
        else:
            encoded_data.append(data[i])
    print(encoded_data)
    return_data=[]
    for attr in atributos:
        if attr == "totalScore":
            return_data.append(encoded_data[0])
        if attr == "POSx":
            return_data.append(encoded_data[1])
        if attr == "POSy":
            return_data.append(encoded_data[2])
        if attr == "module":
            return_data.append(encoded_data[3])
        if attr == "angle":
            return_data.append(encoded_data[4])
        if attr == "direction":
            return_data.append(encoded_data[5])
        if attr == "wall_ahead":
            return_data.append(encoded_data[6])
        if attr == "G1_POSX":
            return_data.append(encoded_data[7])
        if attr == "G1_POSY":
            return_data.append(encoded_data[8])
        if attr == "G2_POSX":
            return_data.append(encoded_data[9])
        if attr == "G2_POSY":
            return_data.append(encoded_data[10])
        if attr == "G3_POSX":
            return_data.append(encoded_data[11])
        if attr == "G3_POSY":
            return_data.append(encoded_data[12])
        if attr == "G4_POSX":
            return_data.append(encoded_data[13])
        if attr == "G4_POSY":
            return_data.append(encoded_data[14])
        if attr == "ALIVE_G1":
            return_data.append(encoded_data[15])
        if attr == "ALIVE_G2":
            return_data.append(encoded_data[16])
        if attr == "ALIVE_G3":
            return_data.append(encoded_data[17])
        if attr == "ALIVE_G4":
            return_data.append(encoded_data[18])
        if attr == "ghost_count":
            return_data.append(encoded_data[19])
        if attr == "G1_DIST":
            return_data.append(encoded_data[20])
        if attr == "G2_DIST":
            return_data.append(encoded_data[21])
        if attr == "G3_DIST":
            return_data.append(encoded_data[22])
        if attr == "G4_DIST":
            return_data.append(encoded_data[23])
        if attr == "closest_posX":
            return_data.append(encoded_data[24])
        if attr == "closest_posY":
            return_data.append(encoded_data[25])
        if attr == "G1_CLOSE":
            return_data.append(encoded_data[26])
        if attr == "G2_CLOSE":
            return_data.append(encoded_data[27])
        if attr == "G3_CLOSE":
            return_data.append(encoded_data[28])
        if attr == "G4_CLOSE":
            return_data.append(encoded_data[29])
        if attr == "ghost_is_close":
            return_data.append(encoded_data[30])
    
    return return_data, encoder_action