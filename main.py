from NetworkMeasures import networkMeasures
from GraphConstruction import buildGraphFromAccountData, buildGraphFromHashtagData
from WordCloudGeneration import cloudVisualization

## step 3 network visualization

buildGraphFromAccountData()
buildGraphFromHashtagData()

## step 4 network measures

networkMeasures()

## step 5 content analysis

cloudVisualization()