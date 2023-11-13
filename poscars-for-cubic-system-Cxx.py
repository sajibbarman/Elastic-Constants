import os
import numpy as np
from colorama import Fore, Style, init
import math

init(autoreset=True)

# Function to read 3rd to 5th lines from a text file and store in a 3x3 matrix
def read_lines_and_create_matrix(file_name):
    matrix = [[0.0] * 3 for _ in range(3)]

    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()[2:5]

            for i, line in enumerate(lines):
                elements = line.strip().split()
                matrix[i] = [float(element) for element in elements]

    except FileNotFoundError:
        print(f"{Fore.RED}File '{file_name}' not found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

    return matrix

# Function to perform operations on the matrix and write to new POSCAR files in directories
def perform_operations_and_write_files(base_directory, base_file_name, matrix):
    try:
        # Create C11 directory if it doesn't exist
        c11_directory = os.path.join(base_directory, 'C11')
        os.makedirs(c11_directory, exist_ok=True)

        # Save the original matrix as POSCAR_00 in C11
        original_file_name = os.path.join(c11_directory, f"{base_file_name}_00")
        with open(original_file_name, 'w') as original_file:
            with open(f"{base_file_name}", 'r') as original_content:
                original_file.writelines(original_content.readlines()[:2])

            for row in matrix:
                # Format each element to 8 decimal places
                formatted_row = ["{:.8f}".format(element) for element in row]
                line = " ".join(formatted_row) + "\n"
                original_file.write(line)

            with open(f"{base_file_name}", 'r') as original_content:
                original_file.writelines(original_content.readlines()[5:])

        # Create C12 directory if it doesn't exist
        c12_directory = os.path.join(base_directory, 'C12')
        os.makedirs(c12_directory, exist_ok=True)

        # Update (2,1) as (1,1) * sin(theta) for theta from 0 to 50 degrees in C12
        for theta in range(-5, 55, 5):
            radians_theta = math.radians(theta)
            new_matrix = np.array(matrix)
            new_matrix[1][0] = new_matrix[0][0] * math.sin(radians_theta)

            new_file_name_c12 = os.path.join(c12_directory, f"{base_file_name}_{theta:02}")
            write_matrix_to_file(new_file_name_c12, new_matrix, base_file_name)

        # Create C44 directory if it doesn't exist
        c44_directory = os.path.join(base_directory, 'C44')
        os.makedirs(c44_directory, exist_ok=True)

        # Update (1,0) as (0,0)*sin(theta) and (1,1) as (1,1)*cos(theta) for theta from 0 to 50 degrees in C44
        for theta in range(-5, 55, 5):
            radians_theta = math.radians(theta)
            new_matrix = np.array(matrix)
            new_matrix[1][0] = new_matrix[0][0] * math.sin(radians_theta)
            new_matrix[1][1] = new_matrix[1][1] * math.cos(radians_theta)

            new_file_name_c44 = os.path.join(c44_directory, f"{base_file_name}_{theta:02}")
            write_matrix_to_file(new_file_name_c44, new_matrix, base_file_name)

        # Add and subtract 0.1 from the (1,1) element and create files in C11
        for i in range(1, 6):
            new_matrix = np.array(matrix)
            new_matrix[0][0] += 0.1 * i

            # Use the formatted string for positive numbers
            new_file_name_c11 = os.path.join(c11_directory, f"{base_file_name}_{i:02}")
            write_matrix_to_file(new_file_name_c11, new_matrix, base_file_name)

            new_matrix = np.array(matrix)
            new_matrix[0][0] -= 0.1 * i

            # Use the formatted string for negative numbers
            new_file_name_c11 = os.path.join(c11_directory, f"{base_file_name}_-{i:02}")
            write_matrix_to_file(new_file_name_c11, new_matrix, base_file_name)

    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

# Function to write a matrix to a file, including the original content up to line 2 and from line 6 onwards
def write_matrix_to_file(file_name, matrix, original_file_name):
    with open(file_name, 'w') as new_file:
        with open(original_file_name, 'r') as original_content:
            new_file.writelines(original_content.readlines()[:2])

        for row in matrix:
            # Format each element to 8 decimal places
            formatted_row = ["{:.8f}".format(element) for element in row]
            line = " ".join(formatted_row) + "\n"
            new_file.write(line)

        with open(original_file_name, 'r') as original_content:
            new_file.writelines(original_content.readlines()[5:])

# Example usage:
file_name = 'POSCAR'  # Assuming "POSCAR" is in the same directory
result_matrix = read_lines_and_create_matrix(file_name)

directory_name = '.'  # Change this to your desired base directory
perform_operations_and_write_files(directory_name, 'POSCAR', result_matrix)
