from GraphConstruction import buildGraphFromAccountData
import networkx as nx
from matplotlib import pyplot as plt

### Find the page rank of the user graph

userGraph = buildGraphFromAccountData(False)
userGraphPageRanking = nx.pagerank(userGraph)
plt.hist(list(userGraphPageRanking.values()), bins=15)
plt.title("Distribution of PageRank in User Graph")
plt.savefig("NetworkVisualizations/PageRank.png")

## Find the degree distribution as measure (2)

degreeDist = dict(userGraph.degree())
plt.hist(list(degreeDist.values()), bins=15)
plt.title("Distribution of degree")
plt.savefig("NetworkVisualizations/DegreeDist.png")

## Find the betweenness centrality as measure (3)

betweennessdist = nx.closeness_centrality(userGraph)
# plt.pie(list(betweennessdist.values()))
print(betweennessdist)
plt.hist(list(betweennessdist.values()), bins=15)
plt.title("Distribution of betweenness")
plt.savefig("NetworkVisualizations/BetweennessDist.png")

## plot the histogram of the pagerank


