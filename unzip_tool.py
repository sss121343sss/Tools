import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import pathlib

def select_zip_files():
    """
    Opens a dialog for the user to select multiple .zip files.
    Returns a list of selected file paths.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Define file types for the dialog
    file_types = [("ZIP files", "*.zip"), ("All files", "*.*")]

    # Ask the user to select one or more .zip files
    file_paths = filedialog.askopenfilenames(
        title="Select ZIP files to unzip",
        filetypes=file_types
    )
    root.destroy() # Clean up the hidden root window
    return file_paths

def create_unique_output_folder(base_path, folder_name="unzipped_files"):
    """
    Creates a unique folder name in the base_path.
    If 'folder_name' exists, it appends a number (e.g., folder_name_1, folder_name_2).
    Returns the Path object of the created folder.
    """
    output_path = pathlib.Path(base_path) / folder_name
    counter = 1
    while output_path.exists():
        output_path = pathlib.Path(base_path) / f"{folder_name}_{counter}"
        counter += 1
    
    try:
        output_path.mkdir(parents=True, exist_ok=False) # exist_ok=False to ensure it's a new creation based on logic
        return output_path
    except OSError as e:
        messagebox.showerror("Error", f"Could not create output folder: {output_path}\n{e}")
        return None

def unzip_files(zip_file_paths, output_folder_path):
    """
    Unzips all specified .zip files into the output_folder_path.
    """
    total_files = len(zip_file_paths)
    unzipped_count = 0
    error_files = []

    for i, file_path_str in enumerate(zip_file_paths):
        file_path = pathlib.Path(file_path_str)
        print(f"\nProcessing file {i+1}/{total_files}: {file_path.name}...")
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Extract all contents into the output folder
                zip_ref.extractall(output_folder_path)
                print(f"Successfully extracted '{file_path.name}' to '{output_folder_path}'")
                unzipped_count += 1
        except zipfile.BadZipFile:
            print(f"Error: '{file_path.name}' is not a valid ZIP file or is corrupted.")
            error_files.append(file_path.name + " (Bad ZIP file)")
        except FileNotFoundError:
            print(f"Error: File not found '{file_path.name}'.")
            error_files.append(file_path.name + " (File not found)")
        except Exception as e:
            print(f"An unexpected error occurred with '{file_path.name}': {e}")
            error_files.append(f"{file_path.name} ({e})")
    
    return unzipped_count, error_files

def main():
    """
    Main function to orchestrate the ZIP file selection and extraction process.
    """
    print("Python ZIP File Extractor")
    print("--------------------------")

    # 1. Select ZIP files
    selected_zip_files = select_zip_files()

    if not selected_zip_files:
        print("No ZIP files selected. Exiting.")
        messagebox.showinfo("Information", "No ZIP files were selected.")
        return

    print(f"\nSelected {len(selected_zip_files)} ZIP file(s):")
    for f_path in selected_zip_files:
        print(f"  - {f_path}")

    # 2. Determine the output directory
    # The output directory will be in the same location as the *first* selected ZIP file.
    first_zip_path = pathlib.Path(selected_zip_files[0])
    parent_directory_of_first_zip = first_zip_path.parent

    # 3. Create the output folder
    print(f"\nCreating output folder in: {parent_directory_of_first_zip}")
    output_folder = create_unique_output_folder(parent_directory_of_first_zip, "unzipped_contents")
    
    if not output_folder:
        # Error message already shown by create_unique_output_folder
        return

    print(f"Output folder created: {output_folder}")

    # 4. Unzip the files
    print("\nStarting extraction process...")
    unzipped_count, error_files = unzip_files(selected_zip_files, output_folder)

    # 5. Show summary message
    summary_message = f"Extraction complete.\n\nSuccessfully unzipped: {unzipped_count} file(s).\n"
    if error_files:
        summary_message += f"Failed to unzip/errors with: {len(error_files)} file(s):\n"
        for err_file in error_files:
            summary_message += f"  - {err_file}\n"
    summary_message += f"\nAll extracted contents are in: {output_folder}"

    print("\n--------------------------")
    print(summary_message)
    
    if error_files:
        messagebox.showwarning("Extraction Complete with Errors", summary_message)
    else:
        messagebox.showinfo("Extraction Complete", summary_message)

if __name__ == "__main__":
    # This ensures the script runs when executed directly
    main()
