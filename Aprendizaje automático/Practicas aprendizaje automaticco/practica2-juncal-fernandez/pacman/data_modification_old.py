from sklearn.preprocessing import LabelEncoder

#  CHANGE DATA APPLICATE TO
#   TOTALSCORE  ANGLE   DIRECTON    WALL_AHEAD      ACTION
def change_data_1(data):
    """
    input: data array with especific attributes.
    Customize:
        Change attributes in encoded_data refered to the input. In case the labelEncoder is changed, write your own encoder.
    """
    encoded_data=[data[0],data[4],data[5],data[6]]
    case=[[data[5]]]
    case_2=[[data[6]]]
    #print("case",case)
    encoder_action=LabelEncoder()
    encoder_action.fit(['Stop','East','West','North','South'])
    encoder_bool=LabelEncoder()
    encoder_bool.fit([True,False])
    
    encoded_data[2]=encoder_action.transform(case)
    encoded_data[3]=encoder_bool.transform(case_2)
    return encoded_data, encoder_action