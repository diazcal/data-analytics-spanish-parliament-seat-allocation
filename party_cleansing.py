import numpy as np
import pandas as pd


provinces = ["Tarragona", "Granada"]
df = pd.DataFrame(np.random.randn(2, 2), index=provinces, columns=["PP", "PSOE"])
print(df.filter(like="Granada"))