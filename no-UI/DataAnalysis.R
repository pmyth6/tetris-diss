data = read.csv("log.csv")

#Correct data - game number starts from zero again halfway through
ind = which(data$game.no. == 0)
ind = ind[5]
max.game.1 = data$game.no.[ind-1]
no.obs = length(data$game.no.)
data$game.no.[ind:no.obs] = data$game.no.[ind:no.obs] + max.game.1
max.game = max(data$game.no.)

#Plot the score for each game
plot(seq(1,length(data$game.no.),1), data$score, xlab = "move", ylab = "score")

#Looking at the distribution of moves
table(data$move)
barplot(table(data$move))

#Game Duration (No. moves per game)
count.game.duration = function(data){
  max.game = max(data$game.no.)
  move.count = matrix(0, max.game, 1)
  total.moves = length(data[,1])
  game.count = 0
  for (i in 1:total.moves){
    if (data$game.no.[i] == game.count){
      move.count[data$game.no.[i]+1] = move.count[data$game.no.[i]+1]+1
    }
    else {
      game.count = game.count +1
      move.count[data$game.no.[i]+1] = move.count[data$game.no.[i]+1]+1
    }
  }
  return(count = move.count)
}

game.dur = count.game.duration(data)
plot(seq(1,max.game+1,1), game.dur, type="l", xlab="game number", 
     ylab="number of moves")

#Ratio of vertical:horizontal moves per game
count.ratio = function(data){
  max.game = max(data$game.no.)
  h.count = matrix(0, max.game+1, 1)
  v.count = matrix(0, max.game+1, 1)
  total.moves = length(data[,1])
  game.count = 0
  for (i in 1:total.moves){
    if (data$game.no.[i] == game.count){
      if (substr(data$move[i], 1, 1) == "h"){
        h.count[data$game.no.[i]+1] = h.count[data$game.no.[i]+1]+1
      }
      if (substr(data$move[i], 1, 1) == "v"){
        v.count[data$game.no.[i]+1] = v.count[data$game.no.[i]+1]+1
      }
    }
    else {
      game.count = game.count +1
      if (substr(data$move[i], 1, 1) == "h"){
        h.count[data$game.no.[i]+1] = h.count[data$game.no.[i]+1]+1
      }
      if (substr(data$move[i], 1, 1) == "v"){
        v.count[data$game.no.[i]+1] = v.count[data$game.no.[i]+1]+1
      }
    }
  }
  return(list(hcount = h.count, vcount = v.count, max.game = max.game))
}

ratio = count.ratio(data)
plot(seq(1,max.game+1,1), ratio$vcount/game.dur, type="l", xlab="game number", 
     ylab="ratio v/total", ylim=c(0,1))







