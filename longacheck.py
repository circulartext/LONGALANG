import os
import time
import numpy as np # Used for efficient matrix operations and random number generation
import csv # Used for writing data to CSV files

# Function to generate a random 5x5 matrix
def generate_random_matrix(min_val=1, max_val=10):
    """
    Generates a 5x5 NumPy array (matrix) with random integers within the specified range.
    """
    return np.random.randint(min_val, max_val + 1, size=(5, 5))

# Function to save a list of numbers to a CSV file, each on a new row
def save_to_csv(data_list, filename="longadata.csv"):
    """
    Appends a list of numbers to the specified CSV file, with each number
    written on a new row.
    """
    try:
        with open(filename, 'a', newline='') as csvfile: # 'a' for append mode
            csv_writer = csv.writer(csvfile)
            for item in data_list:
                csv_writer.writerow([item]) # Write each item as a single-element row
        print(f"    Successfully appended {len(data_list)} results to {filename}")
    except IOError as e:
        print(f"    Error writing to CSV file {filename}: {e}")

# --- Matrix Operations and Saving Functions ---

def perform_multiplication_and_save():
    """
    Generates two 5x5 matrices, performs element-wise multiplication,
    and saves each resulting number to longadata.csv.
    """
    print("    Performing 5x5 matrix multiplication...")
    matrix1 = generate_random_matrix()
    matrix2 = generate_random_matrix()
    result_matrix = matrix1 * matrix2 # Element-wise multiplication
    flat_results = result_matrix.flatten().tolist() # Flatten to a 1D list
    print(f"    Matrix 1:\n{matrix1}")
    print(f"    Matrix 2:\n{matrix2}")
    print(f"    Result (element-wise product):\n{result_matrix}")
    save_to_csv(flat_results)

def perform_division_and_save():
    """
    Generates two 5x5 matrices, performs element-wise division,
    handling division by zero, and saves each resulting number to longadata.csv.
    """
    print("    Performing 5x5 matrix division...")
    matrix1 = generate_random_matrix()
    # For matrix2 (divisor), ensure no zeros to prevent ZeroDivisionError
    # We generate numbers from 1 to 10
    matrix2 = generate_random_matrix(min_val=1, max_val=10) # Divisor matrix with no zeros

    # Perform division, handling potential division by zero if matrix2 somehow gets a 0
    # although we've tried to prevent it. np.divide handles this with a warning, but we can be explicit.
    result_matrix = np.divide(matrix1, matrix2, out=np.zeros_like(matrix1, dtype=float), where=matrix2!=0)
    flat_results = result_matrix.flatten().tolist()
    print(f"    Matrix 1:\n{matrix1}")
    print(f"    Matrix 2 (divisor):\n{matrix2}")
    print(f"    Result (element-wise division, 0 if divisor was 0):\n{result_matrix}")
    save_to_csv(flat_results)

def perform_subtraction_and_save():
    """
    Generates two 5x5 matrices, performs element-wise subtraction,
    and saves each resulting number to longadata.csv.
    """
    print("    Performing 5x5 matrix subtraction...")
    matrix1 = generate_random_matrix()
    matrix2 = generate_random_matrix()
    result_matrix = matrix1 - matrix2 # Element-wise subtraction
    flat_results = result_matrix.flatten().tolist()
    print(f"    Matrix 1:\n{matrix1}")
    print(f"    Matrix 2:\n{matrix2}")
    print(f"    Result (element-wise difference):\n{result_matrix}")
    save_to_csv(flat_results)

def perform_addition_and_save():
    """
    Generates two 5x5 matrices, performs element-wise addition,
    and saves each resulting number to longadata.csv.
    """
    print("    Performing 5x5 matrix addition...")
    matrix1 = generate_random_matrix()
    matrix2 = generate_random_matrix()
    result_matrix = matrix1 + matrix2 # Element-wise addition
    flat_results = result_matrix.flatten().tolist()
    print(f"    Matrix 1:\n{matrix1}")
    print(f"    Matrix 2:\n{matrix2}")
    print(f"    Result (element-wise sum):\n{result_matrix}")
    save_to_csv(flat_results)

def check_longastop_files():
    """
    Continuously checks for the existence of longastop1.py, longastop2.py,
    longastop3.py, and longastop4.py. If found, it performs the corresponding
    matrix operation and logs to longadata.csv.
    """
    target_files = {
        "longastop1.py": perform_multiplication_and_save,
        "longastop2.py": perform_division_and_save,
        "longastop3.py": perform_subtraction_and_save,
        "longastop4.py": perform_addition_and_save
    }

    print("Starting file monitoring for longastopX.py files. Press Ctrl+C to stop.")
    print("-" * 70) # Adjusted separator length

    # Keep track of files that have already been processed in the current run,
    # so we don't re-run the matrix operation if the file persists.
    # This state will reset if the script is restarted.
    processed_files_in_current_cycle = set()


    try:
        while True:
            current_check_time = time.strftime('%Y-%m-%d %H:%M:%S')
            status_messages = []
            files_found_this_cycle = set()

            for filename, operation_func in target_files.items():
                if os.path.exists(filename):
                    files_found_this_cycle.add(filename)
                    if filename not in processed_files_in_current_cycle:
                        status_messages.append(f"[{current_check_time}] Found {filename}.")
                        operation_func() # Perform the specific matrix operation
                        processed_files_in_current_cycle.add(filename) # Mark as processed
                    else:
                        status_messages.append(f"[{current_check_time}] {filename} still exists (already processed).")
                else:
                    if filename in processed_files_in_current_cycle:
                        # If a file was processed but now is missing, remove it from processed_files
                        # This allows it to be processed again if it reappears
                        processed_files_in_current_cycle.remove(filename)
                    status_messages.append(f"[{current_check_time}] {filename} is missing.")

            # Print all status messages at once to keep output grouped per check cycle
            for msg in status_messages:
                print(msg)
            print("-" * 70) # Separator for clarity between checks

            time.sleep(2) # Wait for 5 seconds before checking again

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    check_longastop_files()
