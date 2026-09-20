import networkx as nx
import json
import matplotlib.pyplot as plt

def buildGraphFromHashtagData(export=False) -> nx.DiGraph:

    with open("CollectedData/HashtagData.json", "r") as file:
        postData = json.load(file)

    G = nx.DiGraph()

    for toot in postData:
        # Add nodes
        G.add_node(
            toot["id"],
            created_at=toot["created_at"],
            label=toot["content"][:50],
            author=toot["account"]["acct"],
            reblogs=toot["reblogs_count"],
            replies=toot["replies_count"],
            favourites=toot["favourites_count"],
            kind=(
                "boost"
                if toot["reblog"]
                else ("reply" if toot["in_reply_to_id"] else "root")
            ),
            url=toot["url"],
        )

        if toot["in_reply_to_id"] is not None and any(
            [d["id"] == toot["in_reply_to_id"] for d in postData]
        ):
            G.add_edge(toot["id"], toot["in_reply_to_id"])

        elif toot["reblog"] is not None and any(
            [d["id"] == toot["reblog"]["id"] for d in postData]
        ):
            G.add_edge(toot["id"], toot["reblog"]["id"])

    for node in postData:
        G.nodes[node["id"]]["Size"] = (2.71) ** (G.degree(node["id"]))

    if export: nx.write_gexf(G, "GraphFiles/TootGraph.gexf")
    
    return G

def buildGraphFromAccountData(export=False) -> nx.DiGraph:

    with open("CollectedData/UserData.json", "r") as file:
        data = json.load(file)

    for user in data:
        if user["mentioned_by"] is None:
            user["mentioned_by"] = ""

    G = nx.Graph()

    for user in data:
        G.add_node(
            user["id"],
            acct=user["acct"],
            followers_count=user["followers_count"],
            following_count=user["following_count"],
            url=user["url"],
            bot=user["bot"],
            mentioned_by=user["mentioned_by"],
        )

        if user["mentioned_by"] is not None:
            G.add_edge(
                user["id"], user["mentioned_by"]
            )  # For now will only do the mentioned by connection

    if export: nx.write_gexf(G, "GraphFiles/UserGraph.gexf")
    
    return G

### MAIN ###

postGraph = buildGraphFromHashtagData(export=True)
userGraph = buildGraphFromAccountData(export=True)
