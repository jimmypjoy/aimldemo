import pandas as pd
import seaborn as sns  # Why sns?  It's a reference to The West Wing
import matplotlib.pyplot as plt  # seaborn is based on matplotlib
import plotly.express as px

mydata = pd.read_csv("honeyproduction.csv")
#plotly chart
plt.show(px.scatter(mydata, x = 'numcol', y = 'prodvalue', animation_frame = 'year', size = 'totalprod'))