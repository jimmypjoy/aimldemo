import pandas as pd
import seaborn as sns  # Why sns?  It's a reference to The West Wing
import matplotlib.pyplot as plt  # seaborn is based on matplotlib
import plotly.express as px

sns.set(color_codes=True)  # adds a nice background to the graphs

auto = pd.read_csv('Automobile.csv')
print(auto.head())

# to print a histogram for all variables
auto.hist()

# The most convenient way to take a quick look at a univariate distribution in seaborn is the distplot() function. By default, this will draw a histogram and fit a kernel density estimate (KDE).
chart1 = sns.distplot(auto['highway_mpg']);
plt.show()

# without the kde curve
chart1 = sns.distplot(auto['highway_mpg'], kde=False);

# we can turn the kde off and put a tic mark along the x-axis for every data point with rug
chart2 = sns.distplot(auto['city_mpg'], kde=False, rug=True);
plt.show(chart2)

# ## Plotting bivariate distributions
# It can also be useful to visualize a relationship between two variables. The easiest way to do this in seaborn is to use the jointplot() function, which creates a scatterplot of the two variables along with the histograms of each next to the appropriate axes.
chart3 = sns.jointplot(auto['engine_size'], auto['horsepower']);
plt.show(chart3)
# ### Hex Bin Plots
# We can make a hex bin plot that breaks the 2D area into hexagons and the number of points in each hexagon determines the color
chart4 = sns.jointplot(auto['engine_size'], auto['horsepower'], kind="hex");
plt.show(chart4)

# ### Kernel Density Estimation
# We can make a 2D estimation of the density also
chart5 = sns.jointplot(auto['engine_size'], auto['horsepower'], kind="kde");
plt.show(chart5)

# ## Visualizing pairwise relationships in a dataset
# To plot multiple pairwise scatterplots in a dataset, you can use the pairplot() function. This creates a matrix of axes and shows the relationship for each pair of columns in a DataFrame, it also draws the histogram of each variable on the diagonal Axes:
# Be careful about toggle scrolling in the cell menu!!!
chart6 = sns.pairplot(auto[['normalized_losses', 'engine_size', 'horsepower']]);
plt.show(chart6)

# ## Plotting with categorical data
# In a strip plot, the scatterplot points will usually overlap. This makes it difficult to see the full distribution of data. One easy solution is to adjust the positions (only along the categorical axis) using “jitter"
chart7 = sns.stripplot(auto['fuel_type'], auto['horsepower'], jitter=True);
plt.show(chart7)

# A different approach would be to use the function swarmplot(), which positions each scatterplot point on the categorical axis and avoids overlapping points:
chart8 = sns.swarmplot(auto['fuel_type'], auto['horsepower']);
plt.show(chart8)

# ## Boxplots
# Another common graph is a boxplot(). This kind of plot shows the three quartile values of the distribution along with extreme values. The “whiskers” extend to points that lie within 1.5 IQRs of the lower and upper quartile, and then observations that fall outside this range are displayed independently.

chart9 = sns.boxplot(auto['number_of_doors'], auto['horsepower']);
plt.show(chart9)

chart10 = sns.boxplot(auto['number_of_doors'], auto['horsepower'], hue=auto['fuel_type']);
plt.show(chart10)

# ## Bar plots
# We can plot the mean of a a dataset, separated in categories using the barplot() function. When there are multiple observations in each category, it uses bootstrapping to compute a confidence interval around the estimate and plots that using error bars:
# Bar plots start at 0, which can sometimes be practical if zero is a number you want to compare to
chart11 = sns.barplot(auto['body_style'], auto['horsepower'], hue=auto['fuel_type']);
plt.show(chart11)

# A special case for the bar plot is when you want to show the number of observations in each category rather than computing the mean of a second variable. This is similar to a histogram over a categorical, rather than quantitative, variable. In seaborn, it’s easy to do so with the countplot() function:
chart12 = sns.countplot(auto['body_style'], hue=auto['fuel_type']);
plt.show(chart12)

# ## Point plots
# An alternative style for visualizing the same information is offered by the pointplot() function. This function also encodes the value of the estimate with height on the other axis, but rather than show a full bar it just plots the point estimate and confidence interval. Additionally, pointplot connects points from the same hue category. This makes it easy to see how the main relationship is changing as a function of a second variable, because your eyes are quite good at picking up on differences of slopes:
chart13 = sns.pointplot(auto['body_style'], auto['horsepower'], hue=auto['number_of_doors']);
plt.show(chart13)

# ## Drawing multi-panel categorical plots
chart14 = sns.catplot(x="fuel_type",
                      y="horsepower",
                      hue="number_of_doors",
                      col="drive_wheels",
                      data=auto,
                      kind="box");
plt.show(chart14)

# Various types of kind input : {``point``, ``bar``, ``count``, ``box``, ``violin``, ``strip``}
# ## Function to draw linear regression models
# lmplot() is one of the most widely used function to quickly plot the Linear Relationship between 2 variables
chart15 = sns.lmplot(y="horsepower", x="engine_size", data=auto);
plt.show(chart15)

chart16 = sns.lmplot(y="horsepower", x="engine_size", hue="fuel_type", data=auto);
plt.show(chart16)

