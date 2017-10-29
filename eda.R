library(rjson)
data <- fromJSON(file = 'train.json')
#data <- lapply(data, function(x) {
  #x[sapply(x, is.null)] <- NA
  #unlist(x)
#})
df <- data.frame(do.call("rbind", data))
head(df)
#table(unlist(df$cuisine))
barplot(table(unlist(df$cuisine)), las = 2)
#head(df[df$cuisine=='italian',])

for (cuisine in unique(df$cuisine)) {
  cuisine_df <- df[df$cuisine==cuisine,]
  print(cuisine)
  print(head(sort(table(Reduce(c, cuisine_df$ingredients)), decreasing = TRUE), n = 10))
  #by(head(cuisine_df), 1:nrow(head(cuisine_df)), func,dict)
  #print(dict)
  Sys.sleep(5)
}

