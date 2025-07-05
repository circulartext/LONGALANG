import os
import csv
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error # Import for MAE calculation
import time

# --- Data Loading Function ---
def load_data(filepath):
    """
    Loads numerical data from a CSV file (assumed to be a single column).
    Handles file not found errors and non-numeric values.
    """
    data = []
    if not os.path.exists(filepath):
        # print(f"Error: Data file '{filepath}' not found.") # No need to print error if called in a loop
        return None
    try:
        with open(filepath, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row and row[0].strip(): # Ensure row is not empty and first element is not just whitespace
                    try:
                        data.append(float(row[0])) # Assuming single column of numbers
                    except ValueError:
                        print(f"Warning: Skipping non-numeric or empty value found in row: '{row[0].strip()}' in '{filepath}'.")
        if not data:
            # print(f"Warning: No valid numerical data found in '{filepath}'.") # No need if just checking existence
            return None
        return data
    except Exception as e:
        print(f"Error loading data from '{filepath}': {e}")
        return None

# --- Data Preparation for AI Model ---
def create_sequences(data, look_back=5):
    """
    Transforms a 1D list of data into sequences (X) and corresponding next values (y)
    suitable for time series prediction using a supervised learning model.
    X will be a window of `look_back` previous values.
    y will be the value immediately following that window.

    Args:
        data (list): The list of numerical data points.
        look_back (int): The number of previous time steps to use as input features.

    Returns:
        tuple: A tuple containing (X_array, y_array), where X_array is a 2D NumPy array
               (samples, features) and y_array is a 1D NumPy array (targets).
               Returns empty arrays if not enough data.
    """
    X, y = [], []
    if len(data) <= look_back:
        # print(f"  Not enough data ({len(data)} points) to create sequences with look_back={look_back}. "
        #       f"Need at least {look_back + 1} data points for training.")
        return np.array([]), np.array([])

    for i in range(len(data) - look_back):
        # Extract the sequence of 'look_back' previous values
        feature_set = data[i:(i + look_back)]
        # The target is the value immediately after the sequence
        target = data[i + look_back]
        X.append(feature_set)
        y.append(target)

    return np.array(X), np.array(y)

# --- AI Model Training and Inference ---
def train_and_infer_model(data, look_back=5, predict_steps=None):
    """
    Trains a simple Linear Regression model on the provided data and then
    performs autoregressive inference to predict future values.

    Args:
        data (list): The original list of numerical data points.
        look_back (int): The number of previous time steps to use for prediction.
        predict_steps (int, optional): The number of future values to predict.
                                       If None, defaults to len(data) for a full sequence prediction.

    Returns:
        list: A list of predicted future values. Returns an empty list if training
              or inference cannot be performed.
    """
    if predict_steps is None:
        predict_steps = len(data) # Predict as many steps as there are data points

    print(f"\n--- Training AI Model (Look-back window: {look_back}) ---")
    X, y = create_sequences(data, look_back)

    if X.size == 0 or y.size == 0:
        print("  Not enough valid data to train the model. Aborting training and inference.")
        return []

    # Initialize and train the Linear Regression model
    model = LinearRegression()
    model.fit(X, y)
    print(f"  Model training complete. Model coefficients: {model.coef_}, Intercept: {model.intercept_:.4f}")

    # --- Evaluate on Training Data ("get the same results as it was trained on") ---
    print("\n--- Evaluating Model Performance on Training Data ---")
    # Predict the y values based on the X values from the training set
    y_pred_on_train = model.predict(X)
    mae_train = mean_absolute_error(y, y_pred_on_train)
    print(f"  Mean Absolute Error (MAE) on training data: {mae_train:.4f}")
    # You can inspect y and y_pred_on_train for a detailed comparison if needed.

    # --- Inference ---
    print(f"\n--- Performing Inference (Predicting {predict_steps} steps) ---")
    predictions = []
    # To start inference, we need the last 'look_back' elements from the *original* data
    if len(data) < look_back:
        print("  Insufficient historical data to start inference. Aborting.")
        return []
    current_sequence = list(data[-look_back:]) # Copy the last sequence to start prediction

    for i in range(predict_steps):
        # Reshape the current sequence into the format the model expects (1 sample, 'look_back' features)
        input_for_prediction = np.array(current_sequence[-look_back:]).reshape(1, -1)
        predicted_value = model.predict(input_for_prediction)[0]
        predictions.append(predicted_value)
        # Add the newly predicted value to the sequence to use it for the next prediction (autoregressive)
        current_sequence.append(predicted_value)
        print(f"  Predicted step {i+1}: {predicted_value:.4f}")

    print("Inference complete.")
    return predictions

# --- Output Saving Function ---
def save_predictions_to_py_file(predictions, filename="longadataend.py"):
    """
    Saves the list of predicted values to a Python file.
    The file will contain a Python list named 'predicted_data'.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Predicted data generated by longatrain.py on {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("predicted_data = [\n")
            for item in predictions:
                # Format to a reasonable number of decimal places for readability
                f.write(f"    {item:.6f},\n")
            f.write("]\n")
        print(f"\nSuccessfully saved predicted data to '{filename}'")
    except IOError as e:
        print(f"Error saving predictions to '{filename}': {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    DATA_FILE = "longadata.csv"       # The file where longacheck.py outputs results
    OUTPUT_FILE = "longadataend.py"   # The file to save the final predictions
    LOOK_BACK_WINDOW = 5              # Number of previous data points to use for prediction
    CHECK_INTERVAL = 5                # Seconds to wait between checking for the data file

    print("Starting longatrain.py script...")
    print(f"Expected data input from: '{DATA_FILE}'")
    print(f"Output predictions to: '{OUTPUT_FILE}'")

    raw_data = None
    print(f"\nWaiting for '{DATA_FILE}' to be created and contain sufficient data (at least {LOOK_BACK_WINDOW + 1} entries)...")

    try:
        while raw_data is None or len(raw_data) < LOOK_BACK_WINDOW + 1:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            raw_data = load_data(DATA_FILE)
            if raw_data is None:
                print(f"[{current_time}] '{DATA_FILE}' not found or empty. Retrying in {CHECK_INTERVAL} seconds...")
            elif len(raw_data) < LOOK_BACK_WINDOW + 1:
                print(f"[{current_time}] '{DATA_FILE}' found with {len(raw_data)} entries, but need at least {LOOK_BACK_WINDOW + 1}. Retrying in {CHECK_INTERVAL} seconds...")
            else:
                print(f"[{current_time}] '{DATA_FILE}' found with {len(raw_data)} entries. Proceeding with training.")
                break # Exit the loop, data is ready

            time.sleep(CHECK_INTERVAL)

        print(f"Successfully loaded {len(raw_data)} data points from '{DATA_FILE}'.")
        print(f"Raw data sample (first {min(5, len(raw_data))} entries): {raw_data[:min(5, len(raw_data))]}")

        # Train the AI model and perform inference.
        predicted_values = train_and_infer_model(raw_data, look_back=LOOK_BACK_WINDOW, predict_steps=len(raw_data))

        # Output the new list of predictions to the Python file
        if predicted_values:
            save_predictions_to_py_file(predicted_values, OUTPUT_FILE)
        else:
            print("\nNo predictions were generated due to insufficient data or an issue during training/inference.")

    except KeyboardInterrupt:
        print("\nScript interrupted by user (Ctrl+C). Exiting.")
    except Exception as e:
        print(f"\nAn unexpected error occurred during execution: {e}")

    print("\nlongatrain.py finished.")
