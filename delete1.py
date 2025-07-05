# delete_longa1.py
import os
import time

print("Watching for 'longa1.py' to delete... (Press Ctrl+C to stop)")

try:
    while True:
        if os.path.exists("longa1.py"):
            try:
                os.remove("longa1.py")
                print("Deleted longa1.py")
            except Exception as e:
                print(f"Failed to delete longa1.py: {e}")
        else:
            print("No longa1.py found.")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped by user.")
