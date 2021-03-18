import numpy as np
import pandas as pd
from datasets.regions.all import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

print(df_community_and_provice)


# df_party_codes = pd.read_csv("datasets/02201911_MUNI/03021911.DAT")
# provinces = ["Tarragona", "Granada"]
# df = pd.DataFrame(np.random.randn(2, 2), index=provinces, columns=["PP", "PSOE"])
# print(df.filter(like="Granada"))