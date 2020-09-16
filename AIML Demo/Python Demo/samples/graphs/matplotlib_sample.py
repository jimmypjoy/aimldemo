#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

with open("Goals.txt","r") as f:
    HomeTeamGoals = [ int(x) for x in f.readline().strip("\n").strip(" ").split(" ")]
    AwayTeamGoals = [int(x) for x in f.readline().strip("\n").strip(" ").split(" ")]

xVariable = []
ticks = ["Game One", "Game Fifty", "Game 100"]
for i in range(len(HomeTeamGoals)):
    xVariable.append(i)
    
plt.figure(figsize = (10,10))
plt.plot(xVariable, AwayTeamGoals, c = "green", ls = "--",
         label = "Away Team Goals")
plt.title(r"Our first plot $\frac{1}{2}$")
plt.show()
plt.title("Our second plot")
plt.plot(xVariable, HomeTeamGoals, c = "red", ls = ":",
         label = "Home Team Goals")
plt.legend(loc = "upper right")
plt.xlim(0,145)
plt.ylim(-0.5,6)
plt.xlabel(r"Game Number$_5$")
plt.ylabel(r"Goals Scored")
plt.xticks([49],["12/12/12"],rotation = 45)
plt.yticks([3],["Three Goals"],rotation = 90)
plt.text(50,4,r"Our$^3$ Custom Text",fontsize = 8,color = "blue",rotation = 45)
plt.annotate("Text 2", xy = (30,5), xytext = (65,5),
             arrowprops = dict(facecolor = "red",shrink = 25))
plt.savefig("MyFirstFigure.pdf")
plt.show()

##Histogram
TotalGoals = HomeTeamGoals + AwayTeamGoals
plt.figure(figsize = (8,5))
plt.hist(x = (HomeTeamGoals,AwayTeamGoals,TotalGoals),
         bins = range(8),
         label = ["Home Team Goals","Away Team Goals",
         "Total Goals Scored"],
         align = "left")
plt.legend()
plt.xlabel("Goals Scored")
plt.ylabel("Number of goals scored")
plt.show()

plt.figure(figsize = (8,5))
plt.hist2d(x = HomeTeamGoals,
           y = AwayTeamGoals,
           bins = (range(8),range(7)))
plt.xlabel("Home Team Goals")
plt.ylabel("Away Team Goals")
plt.colorbar()
plt.show()
