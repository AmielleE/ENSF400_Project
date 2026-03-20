import tkinter as tk
from tkinter import ttk
import pandas as pd

class DataFrameEditor:
    def __init__(self, dataframe: pd.DataFrame): # DataFrame from the llm-extracted deadlines
        self.df = dataframe

        self.root = tk.Tk()
        self.root.title("On My Agenda - Edit Extracted Deadlines")
        self.root.geometry("600x450")
        self.root.configure(bg="#f5f7fa")

        self.tree = None 
        self.create_widgets() # Create the table to display the DataFrame

        self.root.mainloop()

    def create_widgets(self):
        app_title = tk.Label(self.root, text="On My Agenda", font=("Segoe UI", 22, "bold"), bg="#f5f7fa", fg="#2c3e50")
        app_title.pack(pady=(20, 5))

        subtitle = tk.Label(self.root, text="Review & Edit Extracted Deadlines", font=("Segoe UI", 14), bg="#f5f7fa", fg="#34495e")
        subtitle.pack(pady=(0, 15))

        # Table Frame
        table_frame = tk.Frame(self.root, bg="#f5f7fa")
        table_frame.pack(fill="both", expand=True, padx=20)

        # Scrollbars
        scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        scroll_x = tk.Scrollbar(table_frame, orient="horizontal")

        columns = list(self.df.columns) # Get column names from the DataFrame to set as table headers

        self.tree = ttk.Treeview( table_frame, columns=columns, show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.config(command=self.tree.yview) 
        scroll_x.config(command=self.tree.xview)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # Style the Treeview to match UI design
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview", background="white", foreground="#2c3e50", rowheight=30, fieldbackground="white", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#ecf0f1", foreground="#2c3e50")

        # Columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Insert data
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

        # Double click for editing
        self.tree.bind("<Double-1>", self.edit_cell)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#f5f7fa")
        btn_frame.pack(pady=15)

        save_btn = tk.Button(btn_frame, text="Save Changes", command=self.save_changes, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), width=18, relief="flat")
        save_btn.pack(side="left", padx=10)

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.root.destroy, bg="#e74c3c", fg="white", font=("Segoe UI", 10), width=18, relief="flat")
        cancel_btn.pack(side="left", padx=10)

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

        self.root.destroy()
