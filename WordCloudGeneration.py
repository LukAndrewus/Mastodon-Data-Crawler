from wordcloud import WordCloud
from matplotlib import pyplot as plt
import json

def cloudVisualization():
    with open("KeywordData.json", "r") as file:
        keywords = json.load(file)

    wordcloud = WordCloud(width=1920, height=1080, background_color="white")

    wordcloud.generate_from_frequencies(keywords)

    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation="bilinear") 
    plt.axis("off")
    plt.savefig("NetworkVisualizations/WordCloud-HurricaneHelene")