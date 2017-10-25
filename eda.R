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
func <- function(row) {
  row['ingredients']
}
for (cuisine in unique(df$cuisine)) {
  cuisine_df <- df[df$cuisine==cuisine,]
  by(head(cuisine_df), 1:nrow(head(cuisine_df)), func)
  Sys.sleep(5)
}
