from GraphConstruction import buildGraphFromAccountData
import networkx as nx
from matplotlib import pyplot as plt
import statistics

def networkMeasures():
    ### Find the page rank of the user graph

    userGraph = buildGraphFromAccountData(False)
    userGraphPageRanking = nx.pagerank(userGraph)
    plt.hist(list(userGraphPageRanking.values()), edgecolor="black")
    plt.yscale("log")
    plt.title("Distribution of PageRank")
    plt.savefig("PageRank.png")
    plt.close()
    ## Find the clustering distribution as measure (2)

    clusteringCoeff = nx.clustering(userGraph)
    plt.hist(list(clusteringCoeff.values()), color="brown")
    plt.title("Distribution of Clustering")
    plt.yscale("log")
    plt.savefig("ClusteringDist.png")
    plt.close()

    ## Find the closeness centrality as measure (3)

    closeness = nx.closeness_centrality(userGraph)
    plt.hist(list(closeness.values()), color="green", edgecolor="black", bins=20)
    plt.title("Distribution of Closeness")
    plt.axvline(statistics.mean(closeness.values()), linewidth=2, color="k")
    plt.savefig("Closeness.png")
    plt.close()

    ## One hope relations
    Local_OneHop = [node[1] for node in userGraph.degree()]
    max_degree = max(Local_OneHop)
    min_degree = min(Local_OneHop)
    median_degree = statistics.median(Local_OneHop)
    high_degree = statistics.quantiles(data=Local_OneHop, n=5)

    ## Global 
    Global_average = 2 * userGraph.number_of_edges() / userGraph.number_of_nodes()

    print(f"max degree: {max_degree} + min degree: {min_degree} + median degree: {median_degree} + high degree: {high_degree} + Global average degree: {Global_average}")


