import networkx as nx
import json
import matplotlib.pyplot as plt

with open("HashtagData.json", "r") as file:
    postData = json.load(file)

G = nx.DiGraph()

for toot in postData:
    #Add nodes
    G.add_node(
        toot["id"],
        created_at=toot["created_at"],
        label=toot["content"][:50],
        author=toot["account"]["acct"],
        reblogs=toot["reblogs_count"],
        replies=toot["replies_count"],
        favourites=toot["favourites_count"],
        kind=("boost" if toot["reblog"] else ("reply" if toot["in_reply_to_id"] else "root")),
        url=toot["url"],
    )

    if toot["in_reply_to_id"] is not None and any([d["id"] == toot["in_reply_to_id"] for d in postData]):
        G.add_edge(toot["id"], toot["in_reply_to_id"])

    elif toot["reblog"] is not None and any([d["id"] == toot["reblog"]["id"] for d in postData]):
        G.add_edge(toot["id"], toot["reblog"]["id"])

for node in postData:
    G.nodes[node["id"]]["Size"] = (2.71)**(G.degree(node["id"]))
     
nx.write_gexf(G, "TootGraph.gexf")