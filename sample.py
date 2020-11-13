import numpy as np
from torpido.config.constants import *

m = np.random.uniform(0, 4, 100)
b = np.random.uniform(0, 4, 100)
a = np.random.uniform(0, 4, 100)
t = np.random.uniform(0, 6, 100)

from joblib import dump

dump(list(m), "model/" + RANK_OUT_MOTION)
dump(list(b), "model/" + RANK_OUT_BLUR)
dump(list(a), "model/" + RANK_OUT_AUDIO)
dump(list(t), "model/" + RANK_OUT_TEXT)
