# Importing classes and functions from different modules
from llm_deadline_extraction import extract_deadlines
from dataframe_processing import DataFrameEditor
from ui import FileUploadUI
from file_parser import parse_files
from excel_export import export_to_excel
import tkinter as tk
from tkinter import messagebox

# Load API keys from the .env file
from dotenv import load_dotenv
import os

load_dotenv()

class App(FileUploadUI):
    def __init__(self, root):
        super().__init__(root)

    def process_files(self):
        if not self.files: # Check if any files were uploaded
            messagebox.showwarning("No Files", "Please upload at least one file.")
            return

        try:
            # Parse files 
            parsed_df = parse_files(self.files)

            if parsed_df.empty: # Check if any valid text could be extracted from the uploaded files
                messagebox.showerror("Error", "No valid text could be extracted from files.")
                return

            # LLM extraction
            deadlines_df = extract_deadlines(parsed_df)

            if deadlines_df.empty: # Check if any deadlines were extracted by the LLM
                messagebox.showwarning("No Deadlines Found", "No deadlines were extracted.")
                return

            # Close upload window
            self.root.destroy()

            editor = DataFrameEditor(deadlines_df) # Open dataFrame editor
            updated_df = editor.df # Get edited data

            if updated_df.empty: # Check if the user deleted all rows in the DataFrame editor (no data to export)
                print("No data to export.")
                return

            export_to_excel(updated_df)
            print("Excel file successfully generated!")

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
