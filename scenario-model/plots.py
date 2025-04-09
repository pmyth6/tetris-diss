import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
csv_file_path = '/Users/theahellen/Documents/Uni/Year 4/Dissertation/tetris-diss/tetris-diss/scenario-model/log.csv'
data = pd.read_csv(csv_file_path)

# Plot the 'loss' column against the number of data points
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['loss'])
plt.xlabel('Move number')
plt.ylabel('Loss')
plt.title('Loss over all moves')
plt.grid(True)
plt.show()
