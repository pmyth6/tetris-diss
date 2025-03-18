library(randomcoloR)
library(ggplot2)
library(dplyr)

# Load your dataset
data = read.csv("log.csv")
n = length(data$probability)

mismatched_rows <- which((data$move1 != data$scenario_no1 | data$move2 != data$scenario_no2) & (data$move1 != data$scenario_no2 | data$move2 != data$scenario_no1))  
tail(data[mismatched_rows,])

# Define batch size
batch_size <- 1000  # Define batch size
num_batches <- nrow(data) %/% batch_size  # Number of full batches

# Compute percentages for each batch
percentages <- data %>%
  mutate(batch = rep(1:num_batches, each = batch_size, length.out = nrow(data))) %>%
  group_by(batch) %>%
  summarise(match_percent = mean((move1 == scenario_no1 & move2 == scenario_no2) | (move1 == scenario_no2 & move2 == scenario_no1)) * 100)

# Plot the percentages
ggplot(percentages, aes(x = batch, y = match_percent)) +
  geom_line() +
  geom_point() +
  labs(title = "Percentage of Matches per 1000 Entries",
       x = "Batch Number",
       y = "Percentage Match") +
  theme_bw()

ggsave(filename = "Plots/100neuronlayersLR00081LeakyReLuB.png", plot = last_plot(), width = 8, height = 6, dpi = 300)
