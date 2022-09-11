install.packages("rjson")
library("rjson")

result <- fromJSON(file="./final/analysis_total.json")
print(result)