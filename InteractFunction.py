from code import interact
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import interact
def f(x):
    f=x*2
interact(f,x=(1,2,3,4,5))
print(x * 2)