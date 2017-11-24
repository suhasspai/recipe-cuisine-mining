library(rjson)
library(wordcloud)
library(sets)

data <- fromJSON(file = 'train.json')
df <- data.frame(do.call("rbind", data))
head(df)

# Distribution of recipes among all cuisines

jpeg('cuisine-distribution.jpg', width = 800, height = 600)
barplot(table(unlist(df$cuisine)), las = 2, main = 'Distribution of recipes in each cuisine',
        cex.names = 0.75, xpd = FALSE, xlab = 'Cuisines')
dev.off()

# Top 10 ingredients in each cuisine

ingredients <- set()
top10 <- data.frame(cuisine = character(), ingredients = character(), stringsAsFactors = FALSE)

for (cuisine in unique(df$cuisine)) {
  cuisine_df <- df[df$cuisine == cuisine, ]
  #print(cuisine)
  freq <- sort(table(Reduce(c, cuisine_df$ingredients)), decreasing = TRUE)
  
  # Create wordcloud images
  jpeg(paste(toString(cuisine), 'wordcloud.jpg', sep = '-'), width = 600, height = 600)
  wordcloud(names(freq), freq, max.words = 200, scale = c(6, .1), colors = brewer.pal(6, 'Dark2'))
  dev.off()
  
  ingredients <- set_union(ingredients, as.set(names(head(freq, n = 10))))
  top10[nrow(top10) + 1,] <- c(cuisine, toString(names(head(freq, n = 10))))
}

# Create table of top 10 ingredients in each cuisine
write.csv(file = 'top_10_for_each_cuisine.csv', x = top10)

for (ingredient in ingredients) {
  ingredient_df <- data.frame(cuisine = character(0), relative_freq = numeric(0),
                              stringsAsFactors = FALSE)
  print(ingredient)
  for (cuisine in unique(df$cuisine)) {
    cuisine_df <- df[df$cuisine==cuisine,]
    freq <- sort(table(Reduce(c, cuisine_df$ingredients)), decreasing = TRUE)
    ingredient_df[nrow(ingredient_df) + 1,] <-
      list(toString(cuisine), freq[ingredient]/nrow(cuisine_df))
  }
  
  # Create bar plots for each 'Top 10' ingredient
  jpeg(paste(toString(ingredient), 'barplot.jpg', sep = '-'), width = 800, height = 600)
  barplot(ingredient_df$relative_freq, las = 2, names.arg = ingredient_df$cuisine,
          main = toString(ingredient), cex.names = 0.75)
  dev.off()
}
