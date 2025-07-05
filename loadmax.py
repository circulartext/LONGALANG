# loadmax.py

def select_number():
    """
    Presents a selection of numbers (1 to 4) and returns the user's choice.
    """
    options = [1, 2, 3, 4]
    print("Please select a number from the following options:")
    for option in options:
        print(f"{option}) Option {option}")

    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
            if choice in options:
                return choice
            else:
                print("Invalid selection. Please choose a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")

# --- THIS IS THE CRUCIAL PART THAT NEEDS TO BE AT THE END OF YOUR loadmax.py ---
# This block ensures that select_number() is called when loadmax.py is executed,
# whether directly or when imported and run by another script like loadedmax.py.
if __name__ == "__main__":
    selected_num = select_number()
    print(f"You selected: {selected_num}")

    # --- New code to create a file based on the selected number ---
    file_name = f"longastop{selected_num}.py"
    try:
        with open(file_name, 'w') as f:
            # You can add some default content to the file if needed.
            # For example, to make it a valid, empty Python file:
            f.write(f"# This is longastop{selected_num}.py, created by loadmax.py\n")
            f.write(f"# The number {selected_num} was selected.\n")
            # You can add more specific code here that you want in each file
            # e.g., f.write("print('Hello from longastopX.py')")
        print(f"Successfully created file: {file_name}")
    except IOError as e:
        print(f"Error creating file {file_name}: {e}")
    # --- End of new code ---