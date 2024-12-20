import shutil
import os

def cleanup_output_folder():
    output_dir = "tests/output"
    if os.path.exists(output_dir):
        print(f"Cleaning up: {output_dir}")
        shutil.rmtree(output_dir)
        print("Cleanup completed.")
    else:
        print(f"No output folder found at {output_dir}.")

if __name__ == "__main__":
    # Allow the script to be run standalone
    cleanup_output_folder()