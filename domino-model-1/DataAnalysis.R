data = read.csv("log_50hr9.csv")

#Remove last game as it didn't finish
max.game = max(data$game.no.)
ind.to.remove = which(data$game.no.== max.game, arr.ind = TRUE)
data = data[-c(ind.to.remove),]

plot(data$game.no., data$score, xlab = "game number", ylab = "score")

barplot(table(data$move))

# Create a blank plot
x = 1:5000
y = data$score[1:5000]+100
plot(x, y, type = "n", ylim = c(0, 400 + 5), xlab = "Data Number", ylab = "Score + 100", main = "First 5000 Games")
# Add vertical lines
segments(x0 = x, y0 = 0, x1 = x, y1 = y, col = data$game.no., lwd = 2)

# Create a blank plot
x = 251179:256179
y = data$score[251179:256179]+100
plot(x, y, type = "n", ylim = c(0, 400 + 5), xlab = "Data Number", ylab = "Score + 100", main = "Last 5000 Games")
# Add vertical lines
segments(x0 = x, y0 = 0, x1 = x, y1 = y, col = data$game.no., lwd = 2)







