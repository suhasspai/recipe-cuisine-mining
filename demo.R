data <- read.csv('matrix.csv')
ingredients <- read.csv('top10ings.csv')
x <- data$cuisine
List <- ingredients$ingredient
for (y in List) {
  print(y)
  xx<-barplot(data[[y]], names.arg = x, main = y, xlab = "Cuisine",
              ylab = "Frequency", las = 2, horiz = FALSE, col = "red")
  text(x = xx, y = data[[y]], label = data[[y]], pos = 3, cex = 0.6, col = "black")
  Sys.sleep(5)
}
