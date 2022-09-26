
import numpy as np

listed = list(range(1,6))
combi = np.array(np.meshgrid(listed, listed)).T.reshape(-1,2)
combi = np.sort(combi)
combi = np.unique(combi, axis = 0)
remove = np.array([listed, listed]).T.reshape(-1,2)
combi = [item for item in combi if item[0] != item[1]]
for i, item in enumerate(combi):
    print(i, item)