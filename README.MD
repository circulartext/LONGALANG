# Longa Language Security System

This project demonstrates a method of enhancing security through a series of Python scripts collectively referred to as the "Longa Language." The scripts implement file manipulation, monitoring, and dynamic execution strategies.

## Project Structure

### Scripts and Their Processes

- **longa.py**:
  - **Purpose**: Main controller script. Manages the creation and self-destruction of various scripts to ensure dynamic execution and a clean environment.
  - **Processes**:
    1. Cleans up artifacts from previous runs.
    2. Creates `longa1.py`, which overwrites `longa.py` with its own content and then self-destructs.
    3. Attempts to import and execute `longa1.py`.
    4. If successful, creates `longa2.py` and self-destructs.
    5. If unsuccessful, creates `longamax.py` and executes it to recreate `longa.py`, ensuring a retry.

- **delete_longa1.py**:
  - **Purpose**: Ensures that `longa1.py` is promptly deleted if it exists.
  - **Processes**:
    - Continuously monitors for `longa1.py`.
    - Attempts deletion, providing feedback on success or failure.

- **longacheck.py**:
  - **Purpose**: Monitors for the presence of specific trigger files and performs matrix operations accordingly.
  - **Processes**:
    - Watches for `longastop1.py` through `longastop4.py`.
    - Executes matrix multiplications, divisions, subtractions, and additions based on file detection.
    - Saves results to `longadata.csv`.

- **loadmax.py**:
  - **Purpose**: Provides user interaction for selecting a number (1 to 4) that corresponds to a matrix operation.
  - **Processes**:
    - Prompts the user to select a number.
    - Creates a file (`longastopX.py`) based on the selection, which acts as a trigger for `longacheck.py`.

- **loadedmax.py**:
  - **Purpose**: Automates the invocation of `loadmax.py`.
  - **Processes**:
    - Runs `loadmax.py`, facilitating remote or automated number selection.
    - Self-destructs after execution to maintain a clean system state.

## Installation

Ensure Python is installed on your system. This project requires Python 3 and the following packages:

```bash
pip install numpy