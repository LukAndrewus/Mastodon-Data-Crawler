from GraphConstruction import buildGraphFromAccountData
import networkx as nx
from matplotlib import pyplot as plt

### Find the page rank of the user graph

userGraph = buildGraphFromAccountData(False)
userGraphPageRanking = nx.pagerank(userGraph)
plt.hist(list(userGraphPageRanking.values()), bins=15)
plt.title("Distribution of PageRank in User Graph")
plt.savefig("NetworkVisualizations/PageRank.png")
plt.close()
## Find the degree distribution as measure (2)

clusteringCoeff = nx.clustering(userGraph)
plt.hist(list(clusteringCoeff.values()), bins=30)
plt.title("Distribution of clustering")
plt.savefig("NetworkVisualizations/ClusteringDist.png")
plt.close()

## Find the betweenness centrality as measure (3)

betweennessdist = nx.closeness_centrality(userGraph)
# plt.pie(list(betweennessdist.values()))
plt.hist(list(betweennessdist.values()), bins=15)
plt.title("Distribution of betweenness")
plt.savefig("NetworkVisualizations/BetweennessDist.png")

## plot the histogram of the pagerank


