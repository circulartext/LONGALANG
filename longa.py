# longa.py
# -*- coding: utf-8 -*-
import os
import time
import importlib.util
import subprocess

# Function to read a file's content and encode it safely to ASCII
def get_clean_ascii_code(filepath):
    """
    Reads a file's content, attempts to decode it tolerantly,
    and then encodes it to ASCII, replacing problematic characters.
    This ensures the code can be safely embedded as a string literal.
    """
    # Read as bytes to avoid initial decoding errors
    with open(filepath, "rb") as f:
        raw_bytes = f.read()
    # Decode using a tolerant scheme (latin-1 often works for such errors),
    # then encode to ASCII, replacing problematic characters.
    # Explicitly replace common problem chars like em-dashes if they slip in
    decoded_string = raw_bytes.decode('latin-1', errors='replace')
    # Explicitly replace common problem chars if they still exist after decoding
    decoded_string = decoded_string.replace('—', '--').replace('–', '-')
    return decoded_string.encode('ascii', errors='xmlcharrefreplace').decode('ascii')

def clean_previous_run_artifacts():
    """
    Attempts to delete temporary and generated files from previous runs
    of longa.py, longamax.py, and loadedmax.py.
    This helps ensure a clean state and addresses issues with files not self-destructing.
    """
    files_to_clean = [
        "longa1.py",
        "longa2.py", # longa2.py is created but does not self-destruct, so include for cleanup
        "longamax.py",
        "loadedmax.py"
    ]
    print("\n--- Cleaning up previous run artifacts ---")
    for f_name in files_to_clean:
        if os.path.exists(f_name):
            try:
                os.remove(f_name)
                print(f"  Cleaned up: {f_name}")
            except OSError as e:
                print(f"  Error cleaning up {f_name}: {e} (file might be in use or permissions issue)")
        else:
            print(f"  {f_name} not found (already clean or never created).")
    print("--- Cleanup complete ---\n")


# --- THIS IS THE CRUCIAL PART THAT NEEDS TO BE AT THE END OF YOUR longa.py ---
# This block ensures that longa.py's main logic is executed when run directly.
if __name__ == "__main__":
    # Perform cleanup of potential leftover files from previous runs
    clean_previous_run_artifacts()

    # --- Second 1: Create longa1.py ---
    # longa1.py is designed to overwrite longa.py, and then self-destruct.
    time.sleep(1)

    # Capture the *current* state of longa.py's content for embedding into longa1.py
    current_longa_code_for_longa1 = get_clean_ascii_code(__file__)

    longa1_code = f'''# longa1.py
# -*- coding: utf-8 -*-
# This script is designed to overwrite the original longa.py with its own content.
# The 'code' variable holds the exact content of longa.py at the time longa1.py was created.
code = {current_longa_code_for_longa1!r}

with open("longa.py", "w", encoding="utf-8") as f: # Explicitly write as UTF-8
    f.write(code) # Write the pre-prepared code directly

import os
# Self-destruct longa1.py after it has completed its task
current_script_path = os.path.abspath(__file__) # Get path for the currently running longa1.py
try:
    os.remove(current_script_path)
    print(f"longa1.py self-destruction complete: {{os.path.basename(current_script_path)}} removed.")
except OSError as e:
    print(f"Error during self-destruction of longa1.py ({{os.path.basename(current_script_path)}}): {{e}}")

'''
    # Write the longa1.py script to a file
    with open("longa1.py", "w", encoding="utf-8") as f:
        f.write(longa1_code)

    print("Step 1 complete: longa1.py created.")

    # --- Second 2: Try to import longa1.py ---
    # This attempts to execute longa1.py, which will overwrite the current longa.py.
    time.sleep(1)
    longa1_imported = False
    if os.path.exists("longa1.py"):
        try:
            # Import spec, then load the module
            spec = importlib.util.spec_from_file_location("longa1", "longa1.py")
            longa1 = importlib.util.module_from_spec(spec)
            # Execute the module. This is where longa1.py will overwrite longa.py
            spec.loader.exec_module(longa1)
            print("Step 2 complete: longa1.py imported successfully.")
            longa1_imported = True
        except Exception as e:
            print(f"Step 2: Failed to import longa1.py: {e}")
    else:
        print("Step 2: longa1.py not found.")

    # --- Second 3: Conditional execution based on longa1_imported ---
    time.sleep(1)
    if longa1_imported:
        # This block executes if longa1.py was successfully imported (and thus overwrote longa.py).
        # Only longa2.py is created here. No longamax.py or loadedmax.py.
        with open("longa2.py", "w", encoding="utf-8") as f:
            f.write("# longa2.py created at second 3 after importing longa1.py\n")
            f.write("print('longa2.py has been created.')\n")
        print("Step 3 complete: longa2.py created.")

        # --- Final: longa.py self-destructs when longa1.py imported successfully ---
        # The currently running 'longa.py' process attempts to delete its own file.
        # This can sometimes fail if the OS holds a lock on the file, but it's the intended behavior.
        current_longa_path = os.path.abspath(__file__)
        try:
            os.remove(current_longa_path)
            print(f"longa.py has self-destructed (after longa1 imported) from: {current_longa_path}.")
        except OSError as e:
            print(f"Error during self-destruction of longa.py (after longa1 imported): {e}")
            print(f"longa.py ({os.path.basename(current_longa_path)}) could not be removed automatically.")

    else:
        # This block executes if longa1.py failed to import or wasn't found.
        # This is the recovery path involving longamax.py AND loadedmax.py.
        print("Skipping longa2.py creation -- longa1.py import failed.")

        # Get the current longa.py's code content for longamax.py to recreate it later.
        # This ensures longamax.py always has an ASCII-clean version of longa.py to write.
        current_longa_code_for_longamax = get_clean_ascii_code(__file__)

        # Define the content of longamax.py, embedding the original_longa_template_code
        longamax_code_content = f'''# longamax.py
# -*- coding: utf-8 -*-
import time
import os
import subprocess

print("longamax.py started. Countdown to self-destruct...")
for i in range(3, 0, -1): # Reduced countdown for quicker testing
    print(f"Deleting in {{i}} seconds...")
    time.sleep(1)

# Recreate original longa.py first
# The code for the original longa.py is embedded here directly as a string literal
# It's already ASCII-cleaned by get_clean_ascii_code
original_longa_code_to_write = {current_longa_code_for_longamax!r}

with open("longa.py", "w", encoding="utf-8") as f: # Explicitly write as UTF-8
    f.write(original_longa_code_to_write)
print("longa.py recreated.")

# Delete self (longamax.py)
current_script_path = os.path.abspath(__file__)
try:
    os.remove(current_script_path)
    print(f"longamax.py self-destruction complete: {{os.path.basename(current_script_path)}} removed.")
except OSError as e:
    print(f"Error during self-destruction of longamax.py ({{os.path.basename(current_script_path)}}): {{e}}")

# Run longa.py immediately after longamax.py self-destructs
print("Attempting to run longa.py after longamax.py self-destructs...")
try:
    # subprocess.Popen detaches the process, allowing the parent (this longamax.py instance) to exit cleanly.
    # This is the very last action taken by longamax.py
    subprocess.Popen(["python", "longa.py"],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     text=True, # text=True means stdout/stderr are text, not bytes
                     creationflags=subprocess.DETACHED_PROCESS if os.name == 'nt' else 0)
    print("longa.py launched successfully from longamax.py.")
except Exception as e:
    print(f"Error launching longa.py: {{e}}")
'''
        # Write the longamax.py script to a file
        with open("longamax.py", "w", encoding="utf-8") as f: # Explicitly write as UTF-8
            f.write(longamax_code_content)

        print("longamax.py created because longa1.py import failed.")

        # --- Run longamax.py and WAIT for it to finish (to see countdown) ---
        print("Attempting to run longamax.py...")
        try:
            # Using subprocess.run will block longa.py until longamax.py completes,
            # ensuring all its output (like the countdown) is visible.
            subprocess.run(["python", "longamax.py"], check=True)
            print("longamax.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running longamax.py: {e}")
        except FileNotFoundError:
            print("Python executable not found for longamax.py. Make sure Python is in your PATH.")
        except Exception as e:
            print(f"An unexpected error occurred during longamax.py execution: {e}")


        # --- Create and Run loadedmax.py (ONLY if longa1_imported is FALSE, after longamax.py finishes) ---
        print("\n--- NEW SECTION (longa1_imported FALSE): Creating and Running loadedmax.py ---")
        loadedmax_code_content = """# loadedmax.py
# -*- coding: utf-8 -*-
import os # Added import for os module
import subprocess
import time

print("loadedmax.py started.")

# As requested, attempt to RUN 'loadmax.py' as a separate process.
target_script_path = "loadmax.py"

# Check if the target script file exists before attempting to run.
if os.path.exists(target_script_path):
    try:
        print(f"Attempting to run {target_script_path} from loadedmax.py as a subprocess...")
        # Use subprocess.run to execute loadmax.py.
        # This will block loadedmax.py until loadmax.py finishes.
        subprocess.run(["python", target_script_path], check=True)
        print(f"{target_script_path} executed successfully by loadedmax.py.")
    except Exception as e:
        print(f"Error running {target_script_path} from loadedmax.py: {e}")
else:
    print(f"{target_script_path} not found. Skipping its execution from loadedmax.py.")

print("loadedmax.py finished. Initiating self-destruct.")
# Self-destruct loadedmax.py after it has completed its task
current_loadedmax_script_path = os.path.abspath(__file__)
try:
    os.remove(current_loadedmax_script_path)
    print(f"Self-destruction complete: {os.path.basename(current_loadedmax_script_path)} has been removed.")
except OSError as e:
    print(f"Error during self-destruction of {os.path.basename(current_loadedmax_script_path)}: {e}")
    print("The loadedmax.py script could not be removed automatically.")

"""
        loadedmax_script_name = "loadedmax.py"
        try:
            with open(loadedmax_script_name, "w", encoding="utf-8") as f:
                f.write(loadedmax_code_content)
            print(f"{loadedmax_script_name} created.")

            print(f"Attempting to run {loadedmax_script_name}...")
            subprocess.run(["python", loadedmax_script_name], check=True)
            print(f"{loadedmax_script_name} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running {loadedmax_script_name}: {e}")
        except FileNotFoundError:
            print("Python executable not found for loadedmax.py. Make sure Python is in your PATH.")
        except Exception as e:
            print(f"An unexpected error occurred during loadedmax.py creation/execution: {e}")
        print("--- NEW SECTION END ---")

        # --- longa.py self-destructs after longamax.py and loadedmax.py have completed ---
        current_longa_path = os.path.abspath(__file__)
        try:
            os.remove(current_longa_path)
            print(f"longa.py has self-destructed after longamax.py and loadedmax.py completed from: {current_longa_path}.")
        except OSError as e:
            print(f"Error during self-destruction of longa.py (after longamax/loadedmax): {e}")
            print(f"longa.py ({os.path.basename(current_longa_path)}) could not be removed automatically.")
