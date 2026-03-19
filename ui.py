import tkinter as tk
from tkinter import filedialog, messagebox

SUPPORTED_EXTENSIONS = (".pdf", ".txt")
MAX_FILES = 6 # Up to 6 files can be uploaded at once

class FileUploadUI:
    def __init__(self, root):
        self.root = root
        self.root.title("On My Agenda - Upload Course Outlines")
        self.root.geometry("600x450")
        self.root.configure(bg="#f5f7fa")
        self.files = []

        self.create_widgets()

    def create_widgets(self):
        # Main App Title
        app_title = tk.Label(self.root, text="On My Agenda", font=("Segoe UI", 24, "bold"), bg="#f5f7fa", fg="#2c3e50")
        app_title.pack(pady=(20, 5))

        title = tk.Label(self.root, text="Upload Course Outlines", font=("Segoe UI", 18, "bold"), bg="#f5f7fa", fg="#2c3e50")
        title.pack(pady=(20, 10))

        subtitle = tk.Label(self.root, text="(PDF files only, max 6)", font=("Segoe UI", 10), bg="#f5f7fa", fg="#7f8c8d") # Subtitle for file requirements instructions
        subtitle.pack(pady=(0, 10))

        # Main frame
        frame = tk.Frame(self.root, bg="#f5f7fa")
        frame.pack(pady=10)

        # Upload Button
        upload_btn = tk.Button(self.root, text="Select Files", command=self.select_files, bg="#4a90e2", fg="white", font=("Segoe UI", 11, "bold"), width=20, relief="flat", padx=10, pady=5)
        upload_btn.pack(pady=5)

        # Listbox to show selected files
        self.file_listbox = tk.Listbox(self.root, width=70, height=10, font=("Segoe UI", 10), bg="white", fg="#2c3e50", selectbackground="#4a90e2", bd=0, highlightthickness=1, highlightcolor="#dcdde1")
        self.file_listbox.pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#f5f7fa")
        btn_frame.pack(pady=15)

        # Remove button
        remove_btn = tk.Button(btn_frame, text="Remove Selected", command=self.remove_selected, bg="#e74c3c", fg="white", font=("Segoe UI", 10), width=18, relief="flat")
        remove_btn.pack(side="left", padx=10)

        # Process button
        process_btn = tk.Button( btn_frame, text="Process Files", command=self.process_files, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), width=18, relief="flat")
        process_btn.pack(side="left", padx=10)

    def select_files(self):
        if len(self.files) >= MAX_FILES: # Check if the user has already uploaded the maximum number of files
            messagebox.showwarning("Limit Reached", "You can only upload up to 6 files.")
            return
        
        selected = filedialog.askopenfilenames(
            title="Select Course Outline Files",
            filetypes=[("Supported Files", "*.pdf *.txt")]
        )

        for file in selected:
            if file.lower().endswith(SUPPORTED_EXTENSIONS): # Check if the file has a supported extension (.pdf or .txt)
                if file not in self.files:
                    if len(self.files) < MAX_FILES: # Check if adding this file would exceed the maximum limit
                        self.files.append(file) 
                        self.file_listbox.insert(tk.END, file) # Add the file to the listbox for display
                    else:
                        messagebox.showwarning("Limit Reached", "Max 6 files allowed.")
                        break
            else:
                messagebox.showwarning("Invalid File", f"{file} is not a supported format.")

    def remove_selected(self):
        selected_indices = self.file_listbox.curselection()

        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.files[index]

    def process_files(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please upload at least one file.")
            return

        # Placeholder before backend integration
        messagebox.showinfo("Processing", f"{len(self.files)} file(s) ready for processing.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileUploadUI(root)
    root.mainloop()