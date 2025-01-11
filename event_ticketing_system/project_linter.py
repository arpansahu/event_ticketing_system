import os
import shutil
import subprocess


def delete_pyc_and_pycache(root_dir):
    """Delete all .pyc files and __pycache__ folders in the directory and subdirectories."""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Delete .pyc files
        for file in filenames:
            if file.endswith(".pyc"):
                file_path = os.path.join(dirpath, file)
                print(f"Deleting .pyc file: {file_path}")
                os.remove(file_path)

        # Delete __pycache__ folders
        for dirname in dirnames:
            if dirname == "__pycache__":
                folder_path = os.path.join(dirpath, dirname)
                print(f"Deleting __pycache__ folder: {folder_path}")
                shutil.rmtree(folder_path)


def run_pep8_and_correct_imports(root_dir):
    """Run PEP8, sort imports, and remove unused imports."""
    # Run isort to sort imports
    print("Running isort to sort imports...")
    subprocess.run(["isort", root_dir], check=True)

    # Run autoflake to remove unused imports and variables
    print("Running autoflake to remove unused imports and variables...")
    subprocess.run(
        ["autoflake", "--in-place", "--remove-unused-variables", "--remove-all-unused-imports", "--recursive", root_dir],
        check=True,
    )

    # Run flake8 for PEP8 compliance
    print("Running flake8 to check PEP8 compliance...")
    try:
        subprocess.run(["flake8", root_dir], check=True)
    except subprocess.CalledProcessError as e:
        print("Flake8 found issues:")
        print(e.stdout.decode("utf-8") if e.stdout else "Check terminal output for details.")


if __name__ == "__main__":
    root_directory = os.getcwd()  # Use the current directory
    print(f"Cleaning up directory: {root_directory}")
    delete_pyc_and_pycache(root_directory)
    run_pep8_and_correct_imports(root_directory)
    print("Cleanup complete!")
