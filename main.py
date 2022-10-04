import numpy as np
import pandas as pd
import tensorflow as tf
from processing import Processing as P

p = P("Clean_CLS5Mi/NEW_CUMUL.csv")
print(p.process())

print(len(p))