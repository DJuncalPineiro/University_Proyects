from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from scipy.spatial.distance import cdist

import matplotlib.pyplot as plt
from scipy.io.arff import loadarff
import pandas as pd
import numpy as np
import os 
#from sympy import centroid

from joblib import dump

"""
('Original->', 'East', '   encoded->', 0)
('Original->', 'North', '   encoded->', 1)
('Original->', 'South', '   encoded->', 2)
('Original->', 'Stop', '   encoded->', 3)
('Original->', 'West', '   encoded->', 4)

"""

def most_frequent_action(cluster_elements):
    values, count = np.unique(cluster_elements[:,-1],return_counts=True)
    ind = np.argmax(count)
    if values[ind] == 0:
        action = "East"
    elif values[ind] == 1:
        action = "North"
    elif values[ind] == 2:
        action = "South"
    elif values[ind] == 3:
        action = "Stop"
    elif values[ind] == 4:
        action = "West"
    return action

def encode_dataset(dataset, exp):
    encoder_action=LabelEncoder()
    encoder_action.fit(['Stop','East','West','North','South'])

    encoder_bool=LabelEncoder()
    encoder_bool.fit(['True','False'])

    labels_encoded=list(encoder_action.classes_)
    #for i,clave in enumerate(labels_encoded):
    #    print("Original->",clave,"   encoded->",i)

    for i in range(len(exp)):
        attr = exp[i]
        if attr == "direction" or attr == "action":
            dataset[:,i]=encoder_action.transform(dataset[:,i])
        elif "CLOSE" in attr:
            dataset[:,i]=encoder_bool.transform(dataset[:,i])
        elif "ALIVE" in attr:
            dataset[:,i]=encoder_bool.transform(dataset[:,i])
        elif attr == "ghost_is_close" or attr == "wall_ahead":
            dataset[:,i]=encoder_bool.transform(dataset[:,i])
    return dataset


def pruebas_clustering(dataset, file, experiments, arff_name, save_models = False, plot_elbow = False):
    j = 1
    compiled_distortions = []
    for exp in experiments:    
        
        classifiers=[
        KMeans(1),
        KMeans(2),
        KMeans(3),
        KMeans(4),
        KMeans(5),
        KMeans(6),
        KMeans(7),
        KMeans(8),
        KMeans(9),
        KMeans(10),
        KMeans(11),
        KMeans(12)
        ]

        data_panda=pd.DataFrame(dataset[0])
        names=list(data_panda.columns)
        data_panda_numpy=data_panda.to_numpy()

        x=data_panda[exp]
        x=x.to_numpy()

        x_copy=x.copy()

        """#TEST
        x_copy_test=x_test.copy()
        y_copy_test=y_test.copy()"""

        encoded_x = encode_dataset(data_panda_numpy,names)
        x_copy = encode_dataset(x_copy, exp)

        out_cols=['n_Clusters','Centroids', "labels"]
        out=pd.DataFrame(columns=out_cols)

        file.write("\n\n***************************************EXPERIMENTO {}:***************************************".format(j))

        distortions = []
        for clas in classifiers:
            clas.fit(x_copy)
            distortions.append(sum(np.min(cdist(x_copy, clas.cluster_centers_,'euclidean'), axis=1)) / x_copy.shape[0])
            n_cluster = clas.n_clusters
            labels = clas.labels_
            centroides = clas.cluster_centers_
            name = "experiment"+str(j)+"_c"+str(n_cluster)+"_model"

            out_entry=pd.DataFrame([[clas.n_clusters,clas.cluster_centers_, clas.labels_]],columns=out_cols)
            out=out.append(out_entry)
            file.write("\n\nDataset: {}.arff".format(arff_name))
            file.write("\n -  Model dumped as: /{}/{}.joblib   -\n\n".format(arff_name,name))
            file.write("Number of clusters: {} \n".format(clas.n_clusters))
            file.write(str(centroides.round(3)))
            file.write("\n\n")
            file.write("Clusters mapped to actions:\n\n")

            for i in range(n_cluster):
                cluster_elements = encoded_x[np.where(labels==i)]
                action = most_frequent_action(cluster_elements)
                file.write("Cluster {} -> {}\n".format(i,action))

            if save_models:
                
                dump(clas,"/home/robotica/Escritorio/practica_2/models/prueba_3/{}".format(name))
                print("Saving model {}".format(name))
            file.write("\n-----------------------------------------")

        compiled_distortions.append(distortions)
        j +=1

    if plot_elbow:
        fig, axes = plt.subplots(nrows=2,ncols=5)
        
        axes[0, 0].plot(range(1, 13), compiled_distortions[0], marker='o')
        axes[0, 1].plot(range(1, 13), compiled_distortions[1], marker='o')
        axes[0, 2].plot(range(1, 13), compiled_distortions[2], marker='o')
        axes[0, 3].plot(range(1, 13), compiled_distortions[3], marker='o')
        axes[0, 4].plot(range(1, 13), compiled_distortions[4], marker='o')
        axes[1, 0].plot(range(1, 13), compiled_distortions[5], marker='o')
        axes[1, 1].plot(range(1, 13), compiled_distortions[6], marker='o')
        axes[1, 2].plot(range(1, 13), compiled_distortions[7], marker='o')
        axes[1, 3].plot(range(1, 13), compiled_distortions[8], marker='o')
        axes[1, 4].plot(range(1, 13), compiled_distortions[9], marker='o')
        
        axes[0, 0].set_title("Experimento 1")
        axes[0, 1].set_title("Experimento 2")
        axes[0, 2].set_title("Experimento 3")
        axes[0, 3].set_title("Experimento 4")
        axes[0, 4].set_title("Experimento 5")
        axes[1, 0].set_title("Experimento 6")
        axes[1, 1].set_title("Experimento 7")
        axes[1, 2].set_title("Experimento 8")
        axes[1, 3].set_title("Experimento 9")
        axes[1, 4].set_title("Experimento 10")
        
        plt.show()
        
        #t=out.sort_values(by=['Clusters'],ascending=True)
 
 

dataset=loadarff("./training/prueba_3/prueba_3.arff")



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

try:
    file = open("cluster_info.txt", "ax")
except IOError:
    file = open("cluster_info.txt", "a")

pruebas_clustering(dataset, file, experiments, "prueba_3", save_models = False, plot_elbow= True)


"""
for arff in arffs:
    dataset=loadarff("./training/"+str(arff))
    pruebas_clustering(dataset, file, experiments, arff, save_models = False)
"""



























