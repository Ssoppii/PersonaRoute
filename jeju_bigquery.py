import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

mbti_df = pd.read_csv('mbti_new.csv', header=0)

# SQL을 사용하여 프로젝트에서 데이터를 조회 후 pandas dataframe에 입력

mbti_np = mbti_df.to_numpy()

# SUM
IF_np = np.zeros((mbti_df.shape[1]-2,), dtype=float)
EF_np = np.zeros((mbti_df.shape[1]-2,), dtype=float)
IT_np = np.zeros((mbti_df.shape[1]-2,), dtype=float)
ET_np = np.zeros((mbti_df.shape[1]-2,), dtype=float)
total_np = np.zeros((mbti_df.shape[1]-2,), dtype=float)
count = [0.0, 0.0, 0.0, 0.0, 0.0]

IF_row_features = np.array([])
EF_row_features = np.array([])
IT_row_features = np.array([])
ET_row_features = np.array([])

IF_flag = True
EF_flag = True
IT_flag = True
ET_flag = True

mbti_np = mbti_df.to_numpy()

for row in mbti_np:
    row_features = row[2:].astype(dtype=np.float16)
    if row[1] == "IF":
        if IF_flag:
            IF_row_features = row_features
            IF_flag = False
            continue
        IF_np += row_features
        IF_row_features = np.vstack((IF_row_features, np.expand_dims(row_features, axis=0)))
        count[0] += 1
    elif row[1] == "EF":
        if EF_flag:
            EF_row_features = row_features
            EF_flag = False
            continue
        EF_np += row_features
        EF_row_features = np.vstack((EF_row_features, np.expand_dims(row_features, axis=0)))
        count[1] += 1
    elif row[1] == "IT":
        if IT_flag:
            IT_row_features = row_features
            IT_flag = False
            continue
        IT_np += row_features
        IT_row_features = np.vstack((IT_row_features, np.expand_dims(row_features, axis=0)))
        count[2] += 1
    elif row[1] == "ET":
        if ET_flag:
            ET_row_features = row_features
            ET_flag = False
            continue
        ET_np += row_features
        ET_row_features = np.vstack((ET_row_features, np.expand_dims(row_features, axis=0)))
        count[3] += 1
    else:
        print("Something wrong")
    total_np += row_features
    count[4] += 1

IF_np /= count[0]
EF_np /= count[1]
IT_np /= count[2]
ET_np /= count[3]
total_np /= count[4]

IF_std = np.zeros((mbti_df.shape[1]-2,), dtype=float)
EF_std = np.zeros((mbti_df.shape[1]-2,), dtype=float)
IT_std = np.zeros((mbti_df.shape[1]-2,), dtype=float)
ET_std = np.zeros((mbti_df.shape[1]-2,), dtype=float)
total_std = np.zeros((mbti_df.shape[1]-2,), dtype=float)

for row in mbti_np:
    row_features = row[2:].astype(dtype=np.float16)
    if row[1] == "IF":
        IF_std += (row_features - IF_np) ** 2
    elif row[1] == "EF" :
        EF_std += (row_features - EF_np) ** 2
    elif row[1] == "IT" :
        IT_std += (row_features - IT_np) ** 2
    elif row[1] == "ET":
        ET_std += (row_features - ET_np) ** 2
    else:
        print("Something wrong")
    total_std += (row_features - total_np) ** 2

IF_std = np.sqrt((IF_std) / count[0])
EF_std = np.sqrt((EF_std) / count[1])
IT_std = np.sqrt((IT_std) / count[2])
ET_std = np.sqrt((ET_std) / count[3])
total_std = np.sqrt((total_std) / count[4])

IF_normalized = (IF_row_features - IF_np) / IF_std
EF_normalized = (EF_row_features - EF_np) / EF_std
IT_normalized = (IT_row_features - IT_np) / IT_std
ET_normalized = (ET_row_features - ET_np) / ET_std


# Weighting
travel_df = pd.read_csv('travel_mbti_et_1.csv', header=0)

normalized_list = [np.mean(IF_normalized, axis=0), np.mean(IT_normalized, axis=0), np.mean(EF_normalized, axis=0), np.mean(ET_normalized, axis=0)]
lst = []

for i in range(len(normalized_list)):
    for j in range(3-i):
        lst.append(normalized_list[i] - normalized_list[3-j])


# Function (Music -> Travel)
def music_travel(auser_musicstat, normalized_list = normalized_list, travel_df = travel_df):
  user_musicstat = auser_musicstat
  user_musicstat_normalized = (user_musicstat - total_np) / total_std
  user_dist = np.zeros((4,)) # 4 distances
  user_dist_weight = np.zeros((4,)) # 4 weights

  sigma = 100

  for i in range(len(normalized_list)):
      user_dist[i] = np.sum(user_musicstat_normalized - normalized_list[i])

      user_dist_weight[i] = 1 / (user_dist[i] ** 2)

  travel_np = travel_df.iloc[:52, 1:].to_numpy(dtype = np.float16) # 52 X 4
  travel_score = np.sum(np.log(travel_np+np.random.rand(52, 4)*4.5) * np.where(user_dist_weight > 1, user_dist_weight**2*100, np.sqrt(user_dist_weight)*100), axis=1) # 52 X 1
  travel_score_dict = {}

  for i in range(travel_score.shape[0]):
      place = travel_df.iloc[i, 0]
      travel_score_dict[place] = travel_score[i]

  sorted_dict = sorted(travel_score_dict.items(), key = lambda item: item[1], reverse=True)
  travel_score_df = pd.DataFrame(sorted_dict)[:10]

  return travel_score_df


# input data
user_musicstat = np.array((0.59402,0.103220883,0.62362,0.169359886,-6.997,2.372522183,0.5,0.505076272,0.061666,0.056152971,0.142286789,0.199589234,0.160918,0.106532647,0.460604,0.195853411,117.99478,30.08924373,0.014886688,0.049698107))
travel_score_df = music_travel(user_musicstat)
print(travel_score_df)

