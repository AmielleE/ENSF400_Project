import tkinter as tk
from tkinter import ttk
import pandas as pd

class DataFrameEditor:
    def __init__(self, dataframe: pd.DataFrame): # DataFrame from the llm-extracted deadlines
        self.df = dataframe

        self.root = tk.Tk()
        self.root.title("Edit Extracted Deadlines")
        self.root.geometry("800x500")

        self.tree = None 
        self.create_table() # Create the table to display the DataFrame

        self.root.mainloop()

    def create_table(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        columns = list(self.df.columns) # Get column names from the DataFrame

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        # Create columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Insert data
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

        self.tree.pack(fill="both", expand=True)

        # Use double-click for editing
        self.tree.bind("<Double-1>", self.edit_cell)

        # Save button
        save_btn = tk.Button(self.root, text="Save Changes", command=self.save_changes)
        save_btn.pack(pady=10)

    def edit_cell(self, event):
        selected_item = self.tree.focus()
        col = self.tree.identify_column(event.x)

        if not selected_item: # If no item is selected, do nothing
            return

        col_index = int(col.replace("#", "")) - 1 # Convert column number to index

        x, y, width, height = self.tree.bbox(selected_item, col) 

        value = self.tree.item(selected_item)["values"][col_index] 

        entry = tk.Entry(self.tree) # Create an entry widget for editing
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value) 
        entry.focus()

        def save_edit(event): # Save the edited value back to the treeview
            new_value = entry.get()
            values = list(self.tree.item(selected_item)["values"])
            values[col_index] = new_value
            self.tree.item(selected_item, values=values)
            entry.destroy()

        entry.bind("<Return>", save_edit) # Save on Enter key
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def save_changes(self): # Save the changes made in the treeview back to the DataFrame
        new_data = []

        for row_id in self.tree.get_children():
            row = self.tree.item(row_id)["values"]
            new_data.append(row) # Append the edited row to the new_data list

        self.df = pd.DataFrame(new_data, columns=self.df.columns) # Create a new DataFrame with the edited data

        print("Updated DataFrame:")
        print(self.df)

        self.root.destroy()