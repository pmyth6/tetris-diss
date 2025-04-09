import tensorflow as tf
from tensorflow import keras
import numpy as np
import csv

# Create the model
model = keras.models.Sequential()
model.add(keras.Input(shape=(2, 10)))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(80, kernel_initializer='he_normal', 
                                    activation=keras.layers.LeakyReLU(alpha=0.01), use_bias=False))
model.add(keras.layers.Dense(80, kernel_initializer='glorot_normal', 
                                    activation="sigmoid", use_bias=False))
model.add(keras.layers.Dense(80, kernel_initializer='glorot_normal', 
                                    activation="sigmoid", use_bias=False))
model.add(keras.layers.Dense(19, activation="softmax", 
                                    use_bias=False))
optimizer = keras.optimizers.Adam(learning_rate=0.01)

# Allocate the moves
moves = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0", 
         "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]

def valid_scenario(num1, num2):
    invalid_pairs = {
        1: {1, 11},
        10: {10, 19},
        11: {1, 2, 11, 12},
        19: {9, 10, 18, 19}
    }
    if num1 in invalid_pairs and num2 in invalid_pairs[num1]:
        return False
    if 2 <= num1 < 10 and num2 in {num1, num1 + 9, num1 + 10}:
        return False
    if 12 <= num1 < 19 and num2 in {num1 - 10, num1 - 9, num1 - 1, num1, num1 + 1}:
        return False
    return True

# Create the scenarios
def scenario(num1, num2):
    grid = np.ones((2, 10))  # Initialize with ones
    for num in [num1, num2]:
        if num <= 10:
            grid[:, num-1] = 0  # Set both rows to 0 at the index
        else:
            grid[1, num-11:num-9] = 0  # Set two consecutive elements in row 1 to 0
    return grid

# Start the count
move_no = 0

# Play the game
while True:

    # Pick a random scenario
    scenario_num1 = np.random.randint(1, 20)
    scenario_num2 = np.random.randint(1, 20)
    if not valid_scenario(scenario_num1,scenario_num2):
        continue
    grid = scenario(scenario_num1,scenario_num2)

    # Update the count
    move_no += 1
    print(move_no)

    # Convert input to tensor
    grid = tf.convert_to_tensor(grid, dtype=tf.float32)
    grid = tf.expand_dims(grid, axis=0)

    with tf.GradientTape() as tape:
        probabilities1 = model(grid, training=True)
        move_index1 = tf.argmax(probabilities1, axis=1)
        move_probability1 = tf.reduce_max(probabilities1, axis=1)

        grid = grid.numpy()[0]
        if int(move_index1)+1 <= 10:
            grid[:, int(move_index1)] = 1  # Set both rows to 0 at the index
        else:
            grid[1, int(move_index1)-10:int(move_index1)-8] = 1 
        grid = tf.convert_to_tensor(grid, dtype=tf.float32)  # Convert back to TensorFlow tensor
        grid = tf.expand_dims(grid, axis=0)

        # Second move
        probabilities2 = model(grid, training=True)
        move_index2 = tf.argmax(probabilities2, axis=1)
        move_probability2 = tf.reduce_max(probabilities2, axis=1)

        # Convert the final move index to tensor for loss calculation
        scenario_tensor1 = tf.convert_to_tensor([scenario_num1-1], dtype=tf.int64)
        scenario_tensor2 = tf.convert_to_tensor([scenario_num2-1], dtype=tf.int64)

        # Compute loss only once based on the final state after two moves
        loss_firstmove_1 = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=scenario_tensor1, logits=probabilities1)
        loss_firstmove_2 = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=scenario_tensor2, logits=probabilities1)
        loss_secondmove_1 = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=scenario_tensor1, logits=probabilities2)
        loss_secondmove_2 = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=scenario_tensor2, logits=probabilities2)
        loss1 = loss_firstmove_1 + loss_secondmove_2
        loss2 = loss_firstmove_2 + loss_secondmove_1
        loss = min(loss1, loss2)

    # Calculate the gradients
    grads = tape.gradient(loss, model.trainable_weights)

    # Update the model
    optimizer.apply_gradients(zip(grads, model.trainable_weights))

    # Save the model
    model.save("GS80N01LR.keras")

    # Save to csv
    filename = "GS80N01LR.csv"
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass
    
    if not file_exists:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['probability', 'move1', 'move2', 'scenario_no1', 'scenario_no2', 'loss', 'move_no'])
    
    row = [move_probability2.numpy(), int(move_index1)+1,int(move_index2)+1, scenario_num1,scenario_num2, loss.numpy(), move_no]
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)