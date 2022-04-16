import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
from numpy import dot
from numpy.linalg import norm

def get_test_inx(df, food_item):
    test_inx = df.index[df['Category'] == food_item].tolist()
    return test_inx

def get_cluster_from_lifestyle(lifestyle_name):
    lifestyle_to_cluster = {
        "Athletic Lifestyle" : [0,5],
        "Active & Healthy" : [0,5,1],
        "Inactive but healthy choices" : [1,9],
        "Inactive & unhealthy" : [2,8,7,4,6,3]
    }
    return lifestyle_to_cluster[lifestyle_name]

def get_recomm_df(lifestyle_name, food_item, n_neigh = 5):
    df = pd.read_csv('clustered_data.csv')
    test_inx = get_test_inx(df, food_item)
    target_cluster = get_cluster_from_lifestyle(lifestyle_name)
    min_max_scaler = preprocessing.MinMaxScaler()
    target_data = df[ df['cluster'].isin(target_cluster) ]

    test_point = df.iloc[test_inx]
    print(test_point)

    cols_norm = target_data.columns.to_list()
    cols_norm = list(set(cols_norm) - set(['Category','cluster']))
    # target_data[cols_norm] = min_max_scaler.fit_transform(target_data[cols_norm])

    target_data[cols_norm] = target_data[cols_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)

    target_knn_model = NearestNeighbors(n_neighbors=n_neigh).fit(target_data.drop(columns=['Category','cluster']))
    target_nearest_neighbors = target_knn_model.kneighbors(test_point.drop(columns=['Category','cluster']), n_neighbors=2*n_neigh, return_distance=False)[0].tolist()
    
    if test_inx in target_nearest_neighbors:
        target_nearest_neighbors.remove(test_inx)
    
    target_neighbor_datapoints = target_data.iloc[target_nearest_neighbors]

    # add current point
    target_neighbor_datapoints = target_neighbor_datapoints.append(df.iloc[test_inx])

    # suggest in increasing order from the centroid of the target cluster
    target_centroid = target_data.drop(columns=['Category', 'cluster']).mean(axis=0).to_numpy()
    target_neighbor_datapoints['distance'] = target_neighbor_datapoints.drop(columns=['Category', 'cluster']).apply(lambda x : np.linalg.norm(x-target_centroid), axis=1)
    target_neighbor_datapoints = target_neighbor_datapoints.sort_values(by=['distance'])

    # cosine sim - score
    target_neighbor_datapoints['cosine_sim'] = target_neighbor_datapoints.apply(lambda x: dot(x[cols_norm], target_centroid)/(norm(x[cols_norm])*norm(target_centroid)), axis=1)
    target_neighbor_datapoints['score'] = target_neighbor_datapoints.apply(lambda x: x["cosine_sim"]*100, axis=1)

    return target_neighbor_datapoints



    



