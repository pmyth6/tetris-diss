library(randomcoloR)
library(ggplot2)
library(dplyr)

data = read.csv("log.csv") # Load your dataset
n = length(data$probability)

# Find rows where the AI plays the wrong move
mismatch_rows <- which(data$ move == data$scenario_no)
print(tail(mismatch_rows))

# Define batch size
batch_size <- 1000  # Define batch size
num_batches <- nrow(data) %/% batch_size  # Number of full batches

# Compute percentages for each batch
percentages <- data %>%
  mutate(batch = rep(1:num_batches, each = batch_size, length.out = nrow(data))) %>%
  group_by(batch) %>%
  summarise(match_percent = mean(move == scenario_no) * 100)

# Plot the percentages
ggplot(percentages, aes(x = batch, y = match_percent)) +
  geom_line() +
  geom_point() +
  labs(title = "Percentage of Matches per 1000 Entries",
       x = "Batch Number",
       y = "Percentage Match") +
  theme_bw()

ggsave(filename = "Plots/40neuronlayers.png", plot = last_plot(), width = 8, height = 6, dpi = 300)
