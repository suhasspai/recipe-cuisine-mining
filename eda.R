library(rjson)
library(wordcloud)
library(sets)
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
ingredients <- set()

for (cuisine in unique(df$cuisine)) {
  cuisine_df <- df[df$cuisine == cuisine,]
  print(cuisine)
  freq <- sort(table(Reduce(c, cuisine_df$ingredients)), decreasing = TRUE)
  #barplot(head(freq, n = 10), las = 2)
  jpeg(paste(toString(cuisine), 'wordcloud.jpg', sep = '-'), width = 600, height = 600)
  wordcloud(names(freq), freq, max.words = 200, scale = c(6, .1),
            colors = brewer.pal(6, 'Dark2'))
  dev.off()
  ingredients <- set_union(ingredients, as.set(names(head(freq, n = 10))))
  #ingredients <- as.set(ingredients)
  #print(ingredients)
  #by(head(cuisine_df), 1:nrow(head(cuisine_df)), func,dict)
  #print(dict)
  #Sys.sleep(5)
}

for (ingredient in ingredients) {
  ingredient_df <- data.frame(cuisine = character(0), relative_freq = numeric(0),
                              stringsAsFactors = FALSE)
  #print(ingredient_df)
  for (cuisine in unique(df$cuisine)) {
    cuisine_df <- df[df$cuisine==cuisine,]
    #print(cuisine)
    freq <- sort(table(Reduce(c, cuisine_df$ingredients)), decreasing = TRUE)
    #print(freq[ingredient]/nrow(cuisine_df))
    ingredient_df[nrow(ingredient_df) + 1,] <-
      list(toString(cuisine), freq[ingredient]/nrow(cuisine_df))
  }
  print(ingredient_df)
  jpeg(paste(toString(ingredient), 'barplot.jpg', sep = '-'),
       width = 800, height = 600)
  barplot(ingredient_df$relative_freq, las = 2, names.arg = ingredient_df$cuisine,
          main = toString(ingredient))
  dev.off()
  #Sys.sleep(5)
}
