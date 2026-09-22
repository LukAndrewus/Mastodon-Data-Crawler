from GraphConstruction import buildGraphFromAccountData
import networkx as nx
from matplotlib import pyplot as plt

### Find the page rank of the user graph

userGraph = buildGraphFromAccountData()

userGraphPageRanking = nx.pagerank(userGraph)

## Find the degree distribution as measure (2)

degreeDist = dict(userGraph.degree())

## Find the clustering coefficient as measure (3)

clusteringCoeff = nx.clustering(userGraph)

## plot the histogram of the pagerank

plt.hist(list(userGraphPageRanking.values()), bins=15)
plt.title("Distribution of PageRank in User Graph")

plt.savefig("NetworkVisualizations/PageRank.png")
