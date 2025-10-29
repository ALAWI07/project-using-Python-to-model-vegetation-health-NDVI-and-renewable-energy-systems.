import matplotlib.pyplot as plt
import csv
import random
import math

"""
Q1 : Your program should calculate the NDVI for each element in the 4377 by 2312 array, to 3
d.p. using Equation 1. It should then display the first 5 columns of the first 5 rows (5 by 5
array) of the full 4377 by 2312 array computed.
"""
# to solve Q1 we need first to import the data of band_red and band_NI
with open('DataForEx1/data/band_red.csv', 'r') as file:
    read_file = csv.reader(file)
    red_str = list(read_file)


def convert_remove(LIST):
    """
    Convert strings to float and remove the first row and first element of each inner list (if not empty).

    Parameters:
    LIST (list of lists): A list of lists containing string elements.

    Returns:
    list of lists: Updated LIST with string elements converted to float and certain elements removed.
    """

    # Remove the first row of the big list
    LIST.pop(0)

    for i in range(len(LIST)):
        if len(LIST[i]) > 0:
            LIST[i].pop(0)  # Remove the first element of each inner list if it's not empty
        for j in range(len(LIST[i])):
            # Convert to float; assuming empty strings are replaced with 0.0
            LIST[i][j] = float(LIST[i][j]) if LIST[i][j] else 0.0

    return LIST


red_float = convert_remove(red_str)
print(len(red_float))  # to make sure that we have the correct length of the list after removing the index (number
# of arrays)

# Now we need NIR data
with open('DataForEx1/data/band_NIR.csv', 'r') as file:
    read_file = csv.reader(file)
    NIR_str = list(read_file)

NIR_float = convert_remove(NIR_str)

print(len(NIR_float[-1]))  # to make sure that we have the correct length of the list after removing the first inner of
# the sublist


def calculate_ndvi(red_data, NIR_data):
    """
    Calculate the Normalized Difference Vegetation Index (NDVI) for each element in the provided arrays.

    Parameters:
    red_data (list of lists): Contains red band data in a 4377 by 2312 array.
    NIR_data (list of lists): Contains Near-Infrared band data in a 4377 by 2312 array.

    Returns:
    list of lists: NDVI values calculated for each element in the arrays rounded to 3 decimal places.
    """

    ndvi_result = []  # Initialize list to store NDVI values

    # Iterate through the red and NIR data arrays
    for sublist_red, sublist_NIR in zip(red_data, NIR_data):
        sublist_ndvi = []  # List to store NDVI values for the current pair of sublists

        # Calculate NDVI for each element in the sublists
        for red_val, NIR_val in zip(sublist_red, sublist_NIR):
            ndvi_val = (NIR_val - red_val) / (NIR_val + red_val)
            ndvi_val = round(ndvi_val, 3)  # Round NDVI value to 3 decimal places
            sublist_ndvi.append(ndvi_val)  # Append NDVI to the sublist_ndvi list

        ndvi_result.append(sublist_ndvi)  # Append the sublist_ndvi to ndvi_result

    return ndvi_result


# Calculate NDVI for the provided red and NIR data
ndvi_result = calculate_ndvi(red_float, NIR_float)

# Display the first 5 columns of the first 5 rows (5 by 5 array) of the calculated NDVI

for i in range(5):
    print(ndvi_result[i][:5])
print('finished answer Q1 Ex1')

"""
Q2 :Your program should display the number of array elements in each category shown in Table1.
"""

Non_vegetated = 0
Low_vegetation = 0
Medium_vegetation = 0
High_vegetation = 0
Very_high_vegetation = 0
# we took the conditions from table 1
for i in ndvi_result:
    for j in i:
        if j < 0:
            Non_vegetated += 1
        elif 0 <= j < 0.3:
            Low_vegetation += 1
        elif 0.3 <= j < 0.6:
            Medium_vegetation += 1
        elif 0.6 <= j < 0.9:
            High_vegetation += 1
        else:
            Very_high_vegetation += 1
print('Non_vegetated =', Non_vegetated)
print('Low_vegetation =', Low_vegetation)
print('Medium_vegetation =', Medium_vegetation)
print('High_vegetation =', High_vegetation)
print('Very_high_vegetation =', Very_high_vegetation)

print('finished answer Q2 Ex1')


"""Q3 : Your program should calculate and display the predicted NDVIp values, to 3 d.p. for the year 2019, using the SWP
 values in Table 2 and Equation 2."""
SWP_2019 = [-2.196, -2.511, -2.261, -3.964, -3.078] # This is the values in table 2

def NDVIp(variable):
    """
    Calculate the NDVI percentage transformation for a single value or a list of values.

    Parameters:
    variable (list or int or float): Input value or list of values to perform NDVI percentage transformation.

    Returns:
    list or float or str: Transformed NDVI values (if list or single value) or an error message.
    """

    if isinstance(variable, list):
        NDVIp_result = []
        for i in range(len(variable)):
            x = (0.26 * variable[i]) + 0.96
            y = round(x, 3)
            NDVIp_result.append(y)
        return NDVIp_result
    elif isinstance(variable, (int, float)):
        return (0.26 * variable) + 0.96
    else:
        return "The variable is neither a list nor a number."


NDVIp_2019 = NDVIp(SWP_2019)
print(NDVIp_2019)
print('finished answer Q3 Ex1')
"""
4. Your program should compute the root mean square error (RMSE) shown in Equation(3) between the predicted
NDVIp values (computed in Question 3) and NDVI values found in Question 1), for 2019.
The (x, y) location shown in Table 2 ,Your program should display the RMSE to 3 d.p.
"""
NDVI_2019 = [ndvi_result[1100][605], ndvi_result[500][3712], ndvi_result[1072][2124], ndvi_result[85][196],
             ndvi_result[2241][4100]] # from table 2
print(NDVI_2019)


def RMSE(list_predicted, list_measured):
    """
    Calculate the Root Mean Squared Error (RMSE) between two lists of predicted and measured values.

    Parameters:
    list_predicted (list): List containing predicted values.
    list_measured (list): List containing measured or actual values.

    Returns:
    float or str: RMSE value if lists have the same length, otherwise an error message.
    """

    if len(list_predicted) == len(list_measured):
        N = len(list_predicted)
        z = 0

        # Calculate the squared difference between predicted and measured values
        for i in range(N):
            z += (list_predicted[i] - list_measured[i]) ** 2

        # Calculate the RMSE value
        r = ((1 / len(list_predicted)) * z) ** 0.5
        return round(r, 3)
    else:
        return 'Arrays do not have the same length'


RMSE_result = RMSE(NDVIp_2019, NDVI_2019)
print(RMSE_result)
print('finished answer Q4 Ex1')

"""
Q5: Your program should output a line plot showing the NDVIp (vertical axis) for each year
(horizontal axis), using the information in Table 2. The data for each location should be
displayed as a separate line on the plot, shown on the same axis. Finally, your program
should save the plot as a file with the name ex1_question5.png.
"""
# from table 2
SWP_2020 = [-1.974, -2.169, -2.154, -3.399, -2.473]
SWP_2021 = [-1.82, -2.01, -1.929, -2.745, -2.423]
SWP_2022 = [-1.772, -1.63, -1.649, -2.648, -2.129]
#by using NDVIp function from Q3
NDVIp_2020 = NDVIp(SWP_2020)
print(NDVIp_2020)
NDVIp_2021 = NDVIp(SWP_2021)
print(NDVIp_2021)
NDVIp_2022 = NDVIp(SWP_2022)
print(NDVIp_2022)

#data for each location should be displayed as a separate line on the plot
data = {
    'POINT 1': {'years': [2019, 2020, 2021, 2022], 'NDVIp': [NDVIp_2019[0], NDVIp_2020[0], NDVIp_2021[0], NDVIp_2022[0]]},
    'POINT 2': {'years': [2019, 2020, 2021, 2022], 'NDVIp': [NDVIp_2019[1], NDVIp_2020[1], NDVIp_2021[1], NDVIp_2022[1]]},
    'POINT 3': {'years': [2019, 2020, 2021, 2022], 'NDVIp': [NDVIp_2019[2], NDVIp_2020[2], NDVIp_2021[2], NDVIp_2022[2]]},
    'POINT 4': {'years': [2019, 2020, 2021, 2022], 'NDVIp': [NDVIp_2019[3], NDVIp_2020[3], NDVIp_2021[3], NDVIp_2022[3]]},
    'POINT 5': {'years': [2019, 2020, 2021, 2022], 'NDVIp': [NDVIp_2019[4], NDVIp_2020[4], NDVIp_2021[4], NDVIp_2022[4]]}
}
# Plotting
plt.figure(figsize=(6, 4))

for point, values in data.items():
    plt.plot(values['years'], values['NDVIp'], label='point')

plt.xlabel('Years')
plt.ylabel('NDVIp')
plt.title('NDVIp for Each Year and point')
plt.legend()
plt.grid(True)

# Save the plot as ex1_question5.png
plt.savefig('ex1_question5.png')

# Display the plot
#plt.show()

print("finished answer Ex1 Q5")