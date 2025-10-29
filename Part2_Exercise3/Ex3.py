import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import random
def calculate_agreement(population, row, col, H=0.0):
    n_rows, n_cols = population.shape
    neighbors_indices = [
        ((row - 1) % n_rows, col),  # Up
        (row, (col - 1) % n_cols),  # Left
        (row, (col + 1) % n_cols),  # Right
        ((row + 1) % n_rows, col)   # Down
    ]
    neighbors_values = [population[r, c] for r, c in neighbors_indices]
    cell_current_value = population[row, col]
    # Sum of products to calculate agreement/disagreement
    agreement = sum(cell_current_value * value for value in neighbors_values)
    # Include external field effect
    agreement += cell_current_value * H
    return agreement
def ising_step(population, H=0.0, alpha=0.1):  # Default alpha to prevent division by zero
    n_rows, n_cols = population.shape
    row = np.random.randint(0, n_rows)
    col = np.random.randint(0, n_cols)
    agreement = calculate_agreement(population, row, col, H)

    # Flip logic based on agreement
    if agreement < 0:
        population[row, col] *= -1
    elif alpha > 0:  # Check to avoid division by zero
        probability = math.exp(-abs(agreement) / alpha)
        random_float = random.random()
        if probability > random_float:
            population[row, col] *= -1

    return population
def plot_ising(im, population):
    new_im = np.array([[0 if val == 1 else 255 for val in row] for row in population], dtype=np.uint8)
    im.set_data(new_im)
    plt.draw()
    plt.pause(0.1)  # Pause to update the plot visually
def ising_main(population, alpha=0.01, H=0.1):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    im = ax.imshow(population, interpolation='none', cmap='gray')  # Use gray scale for better contrast
    for frame in range(100):
        for step in range(1000):
            ising_step(population, H, alpha)
        print('Step:', frame, end='\r')
        plot_ising(im, population)
    plt.show()  # Ensure the plot is shown at the end

# Usage
pop = -np.ones((100, 100))
ising_main(pop, 0.01, 0.1)

