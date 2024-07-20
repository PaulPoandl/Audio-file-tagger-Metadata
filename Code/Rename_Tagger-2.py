import os
import re
from tkinter import Tk, filedialog

def choose_directory():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    root.destroy()
    return folder_selected

def remove_parentheses(text):
    return re.sub(r'\s*\(.*?\)', '', text).strip()

def rename_files(directory):
    for file_name in os.listdir(directory):
        new_name = remove_parentheses(file_name)
        if new_name != file_name:
            os.rename(os.path.join(directory, file_name), os.path.join(directory, new_name))
            print(f"Renamed: {file_name} -> {new_name}")

def main():
    num_directories = int(input("Enter the number of directories you want to rename (1-10): "))
    if num_directories < 1 or num_directories > 10:
        print("Invalid input. Exiting.")
        return

    for _ in range(num_directories):
        directory = choose_directory()
        if not directory:
            print("No directory selected. Skipping.")
            continue

        rename_files(directory)

if __name__ == "__main__":
    main()
